import numpy as np
import scipy.io.wavfile as wav

def filterbanks(filepath,power_spectrum):
    filepath = 'crickets.wav'
    sample_rate,data = wav.read(filepath)
    
    # number of filters
    num_filters = 26
    
    # Convert Hz to Mel
    low_freq_mel = 0
    
    # the max frequency is half the sampling rate (in Hz)
    high_freq_mel = (2595 * np.log10(1 + (sample_rate / 2) / 700))
    
    # generate equally spaced points in the Mel scale
    # n-filters ==> n+2 points
    mel_points = np.linspace(low_freq_mel, high_freq_mel, num_filters + 2)
    
    # convert Mel points to Hertz
    hz_points = (700 * (10**(mel_points / 2595) - 1))
    
    NFFT = 512
    
    # N-point FFT discretizes frequencies from 0 to sample_rate
    # So we divide it into N bins
    # Now we check to which bin our hz_points correspond to 
    bin = np.floor((NFFT + 1) * hz_points / sample_rate)
    
    # create filter banks
    fbank = np.zeros((num_filters, int(np.floor(NFFT / 2 + 1))))
    
    for m in range(1, num_filters + 1):
        f_m_minus = int(bin[m - 1])   # left
        f_m = int(bin[m])             # center
        f_m_plus = int(bin[m + 1])    # right

        for k in range(f_m_minus, f_m):
            fbank[m - 1, k] = (k - bin[m - 1]) / (bin[m] - bin[m - 1])
        for k in range(f_m, f_m_plus):
            fbank[m - 1, k] = (bin[m + 1] - k) / (bin[m + 1] - bin[m])
    filter_banks = np.dot(power_spectrum, fbank.T)
    filter_banks = np.where(filter_banks == 0, np.finfo(float).eps, filter_banks)  # Numerical Stability
    filter_banks = 20 * np.log10(filter_banks)  # dB