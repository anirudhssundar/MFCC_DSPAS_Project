import numpy as np
import scipy.io.wavfile as wav

def preemphasis(signal, coeff=0.95):
    """perform preemphasis on the input signal.
    :param signal: The signal to filter.
    :param coeff: The preemphasis coefficient. 0 is no filter, default is 0.95.
    :returns: the filtered signal.
    """
    return np.append(signal[0], signal[1:] - coeff * signal[:-1])



rate,data = wav.read('crickets.wav')

data2 = preemphasis(data,coeff=0.95)
data2 = data2[1:]
