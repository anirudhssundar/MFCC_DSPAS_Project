function [ mfcc_reqd,flag ] = Calc_MFCC( filepath )
addpath('E:/Scholastic/NITK/Year_3_NITK/Sem-5/Audio Signal Processing/MFCC/MATLAB_Code/')


[y,rate] = audioread(filepath,'native');
sig_dim = size(y);
signal_length = sig_dim(1);

y = double(y);



%%%%%%%%%%%%%%%%%%%%%%%% preprocessing %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%Pre emphasis of the signal y(n) = x(n) - 0.95*x(n):
B = [1 -0.97];
emphasized_signal = filter(B,1,y);

emphasized_signal = emphasized_signal(abs(emphasized_signal) > 500);
x = isempty(emphasized_signal)
if(isempty(emphasized_signal))
    mfcc_reqd = 0;
    flag = 0;
elseif(length(emphasized_signal)<400)
    mfcc_reqd = 0;
    flag = 0;
else
    frame_size = 0.025 ;%25 ms
    frame_overlap = 0.015; %15 ms
    frame_stride = 0.01; %10ms

    %length of one frame (in samples)
    frame_length = (round(frame_size*rate));
    frame_step = (round(frame_stride*rate));
    frame_overlap_sam = round(frame_overlap*rate);

    NFFT = 512 ;
    wnd = hamming(frame_length,'periodic');

    [S, F, T, P] = spectrogram (emphasized_signal, wnd,frame_overlap_sam, NFFT);

    %P is the power frames that we require

    %%%%%%%%%%%%%%%%%%%%%%%% end of pre-processing %%%%%%%%%%%%%%%%%%%%%%%%%%%%

    %%%%%%%%%%%%%%%%%%%%%%%%%  mel filter%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


    %number of filters
    num_filters = 26;

    % Convert Hz to Mel
    low_freq_mel = 0;

    % the max frequency is half the sampling rate (in Hz)
    high_freq_mel = (2595 * log10(1 + (rate / 2) / 700));

    % generate equally spaced points in the Mel scale
    % n-filters ==> n+2 points
    mel_points = linspace(low_freq_mel, high_freq_mel, num_filters + 2);

    % convert Mel points to Hertz
    hz_points = (700 * (10.^(mel_points / 2595) - 1));

    % N-point FFT discretizes frequencies from 0 to sample_rate
    % So we divide it into N bins
    % Now we check to which bin our hz_points correspond to 
    bin = floor((NFFT + 1) * hz_points / rate);


    % create filter banks
    fbank = zeros(num_filters, (floor(NFFT / 2 + 1)));

    for m = 2:num_filters+1
        f_m_minus = (bin(m - 1));  %left
        f_m = (bin(m));             %center
        f_m_plus = (bin(m + 1));    %right

        for k = f_m_minus : f_m
            fbank(m - 1, k+1) = (k - bin(m - 1)) / (bin(m) - bin(m - 1));
        end
        for k = f_m : f_m_plus
            fbank(m - 1, k+1) = (bin(m + 1) - k) / (bin(m + 1) - bin(m));
        end
    end

    P_T = P';
    filter_banks = mtimes(P_T, fbank');
    %filter_banks = where(filter_banks == 0, np.finfo(float).eps, filter_banks)
    filter_banks = 20 * log10(filter_banks);  %dB

    %%%%%%%%%%%%%%%%%%%%%%%%%% end of mel-scale %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


    %%%%%%%%%%%%%%%%%% discrete cosine transform %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    % do the MFCC along the columns
    mfcc = dct(filter_banks');

    % transpose again
    mfcc = mfcc';

    % keep coeffs 2-13
    num_coeffs = 12;

    mfcc_reqd = mfcc(:,2:num_coeffs+1);
    flag = 1;
end

end

