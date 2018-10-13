import numpy as np
import scipy.io.wavfile as wav


def preemphasis(signal, coeff=0.95):
    return np.append(signal[0], signal[1:] - coeff * signal[:-1])


rate,signal = wav.read('crickets.wav')
signal_length = len(signal)


# pre_emphasis
pre_emphasis_coeff = 0.97
emphasized_signal = np.append(signal[0], signal[1:] - pre_emphasis_coeff * signal[:-1])

#create_frames

frame_size = 0.025 #25 ms
frame_overlap = 0.015 #15 ms
frame_stride = 0.01 # 10ms

# length of one frame (in samples)
frame_length =int(round(frame_size*rate))
frame_step = int(round(frame_stride*rate))

# total number of frames
num_frames = int(np.ceil(float(np.abs(signal_length - frame_length)) / frame_step)) 

pad_signal_length = num_frames * frame_step + frame_length
z = np.zeros((pad_signal_length - signal_length))

# append zeros at the end so that all frames have equal samples

pad_signal = np.append(emphasized_signal, z)

# each row contains all the indices of elements to go in one frame
indices = np.tile(np.arange(0, frame_length), (num_frames, 1)) + np.tile(np.arange(0, num_frames * frame_step, frame_step), (frame_length, 1)).T

# each row contains values of all the signal parameters in on frame
frames = pad_signal[indices.astype(np.int32, copy=False)]

# multiply each frame with a hamming window
frames *= np.hamming(frame_length)

# implement 512 point FFT
NFFT = 512
mag_frames = np.absolute(np.fft.rfft(frames, NFFT))
pow_frames = ((1.0 / NFFT) * ((mag_frames) ** 2))
