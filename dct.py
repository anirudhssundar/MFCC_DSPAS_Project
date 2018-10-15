from scipy.fftpack import dct

def dct_value(filter_banks):
    
    # Keep coefficients 2-13
    num_ceps = 12
    
    mfcc = dct(filter_banks, type=2, axis=1, norm='ortho')[:, 1 : (num_ceps + 1)]
    return mfcc
    