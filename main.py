import numpy as np

import preprocess
import mel_scale
import dct

power_spectrum = preprocess.preprocess('crickets.wav')
filter_banks = mel_scale.filter_banks('crickets.wav',power_spectrum)
mfcc = dct.dct_value(filter_banks)
