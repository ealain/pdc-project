# -*- coding: utf-8 -*-

import numpy as np

from config import WAVEFORM_TYPE
from config import SAMPLING_FREQUENCY, BIT_FREQUENCY

from t_encoder import encode

LIST_OF_BITS = encode()
print('Data to be transmitted: ' + str(LIST_OF_BITS))

###   ###   ###   ###   ###   ###   ###

def sin(t):
    '''
    Input: T, evaluation point (seconds)
    Output: value of sine-pulse at time T
    '''
    # Delay between two bits
    bit_period = 1.0/BIT_FREQUENCY
    # Total amount of bits to transmit
    nb_bits = len(LIST_OF_BITS)

    tt = t/bit_period
    i = int(tt) if t > 0 else int(tt)-1
    tt = t - int(tt)*bit_period if int(tt) <= tt else t - (int(tt)-1)*bit_period

    if(i < 0 or i > nb_bits):
        return 0.0
    return (-1 if LIST_OF_BITS[i] == '0' else 1) * np.sin(np.pi*tt/bit_period)


def step(t):
    '''
    Looks for bits produced by encoder and transmits them
    '''
    # Delay between two bits
    bit_period = 1.0/BIT_FREQUENCY
    # Total amount of bits to transmit
    nb_bits = len(LIST_OF_BITS)

    tt = t/bit_period
    i = int(tt) if t > 0 else int(tt)-1
    tt = t - int(tt)*bit_period if int(tt) <= tt else t - (int(tt)-1)*bit_period

    if(i < 0 or i > nb_bits):
        return 0.0
    return -1 if LIST_OF_BITS[i] == '0' else 1


def rootRaisedCosine(t):
    beta = 0.5
    bit_period = 1.0/BIT_FREQUENCY

    if (t== bit_period/(4*beta)):
        return (beta/(np.pi*np.sqrt(2*bit_period)) * \
                ((np.pi + 2)*np.sin(np.pi/(4*beta)) + (np.pi - 2)*np.cos(np.pi/(4*beta))))
    else:
        return (4 * beta / np.pi / np.sqrt(bit_period) * \
            (np.cos((1 + beta) * np.pi * t / bit_period) + \
             (1 - beta) * np.pi / (4 * beta) * np.sinc((1-beta)*t/bit_period)) / \
                (1 - (4*beta*t/bit_period)**2))


def rrc(t, beta = 0.5, truncation = 10):
    '''
    Input: T, evaluation point (seconds)
           BETA, parameter in [0, 1]; greater => slow but reliable transmission
           TRUNCATION, number of period to evaluate; greater => latency but reliance
    Output: value of root-raised-cosine at time T
    '''
    # Delay between two bits
    bit_period = 1/BIT_FREQUENCY
    # Total amount of bits to transmit
    nb_bits = len(LIST_OF_BITS)
    # To be returned (sum of contributions)
    s = 0.0
    # Max value of rrc
    m = 4*beta/np.pi/np.sqrt(bit_period) + (1-beta)/np.sqrt(bit_period) + sum(abs(2*rootRaisedCosine(i*bit_period)) for i in range(1, truncation))

    if(t < - truncation * bit_period  or t >= (nb_bits + truncation) * bit_period):
        # T out of support
        r = 0.0
    else:
        # Bits that will affect function at time T
        relevant_bits = np.zeros(2*truncation+1)
        for i in range(2*truncation+1):
            j = t/bit_period + i - truncation
            j = int(j) if int(j) <= j else int(j) - 1
            if(j >= 0 and j < nb_bits):
                relevant_bits[i] = -1 if LIST_OF_BITS[j] == '0' else 1

        for i in range(2*truncation+1):
            tt = t/bit_period
            tt = t - int(tt)*bit_period if int(tt) <= tt else t - (int(tt)-1)*bit_period
            if(t == bit_period * (1 / 4 / beta + (i - truncation))):
                # L'Hospital's rule because of potential discontinuity
                s += relevant_bits[i] * beta / np.pi / np.sqrt(2*bit_period) * 1 / m * \
                     ((np.pi + 2) * np.sin(np.pi/4/beta) + \
                      (np.pi - 2) * np.cos(np.pi/4/beta))
            else:
                # General case formula
                s += relevant_bits[i] * 4*beta/np.pi/np.sqrt(bit_period) * 1 / m * \
                     (np.cos((1 + beta) * np.pi * ((tt / bit_period - (i-truncation)))) + \
                      (1 - beta) * np.pi / 4 / beta * \
                      np.sinc((1 - beta) * (tt / bit_period - (i-truncation))))/ \
                      (1 - (4*beta*(tt / bit_period - (i-truncation)))**2)

    return s

###   ###   ###   ###   ###   ###   ###

if(WAVEFORM_TYPE == 'sinus'):
    f = sin
elif(WAVEFORM_TYPE == 'rectangle'):
    f = step
elif(WAVEFORM_TYPE == 'rrc'):
    f = rrc
