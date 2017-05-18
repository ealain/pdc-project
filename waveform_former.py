import numpy as np

from config import CODING_METHOD

from encoder import encode


###   ###   ###   ###   ###   ###   ###

def sin_to_01(t):
    return (np.sin(t) + 1) / 2

def bits(t, period = 0.5):
    '''
    Looks for bits produced by encoder and transmits them
    for given PERIOD in seconds
    '''
    list_of_bits = encode()
    i_max = len(list_of_bits) - 1
    i = 0
    while(t - i*period > 0 and i < i_max):
        i += 1
    return float(list_of_bits[i])

###   ###   ###   ###   ###   ###   ###

if(CODING_METHOD == 'test_sinus'):
    f = sin_to_01
elif(CODING_METHOD == 'ascii'):
    f = bits
