# -*- coding: utf-8 -*-

import numpy as np

from config import WAVEFORM_TYPE, TRUNCATION, BETA
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
    bit_period = 1/BIT_FREQUENCY
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
    bit_period = 1/BIT_FREQUENCY
    # Total amount of bits to transmit
    nb_bits = len(LIST_OF_BITS)

    tt = t/bit_period
    i = int(tt) if t > 0 else int(tt)-1
    tt = t - int(tt)*bit_period if int(tt) <= tt else t - (int(tt)-1)*bit_period

    if(i < 0 or i > nb_bits):
        return 0.0
    return -1 if LIST_OF_BITS[i] == '0' else 1


def rootRaisedCosine(t):
    bit_period = 1/BIT_FREQUENCY

    if (t== bit_period/(4*BETA)):
        return (BETA/(np.pi*np.sqrt(2*bit_period)) * \
                ((np.pi + 2)*np.sin(np.pi/(4*BETA)) + (np.pi - 2)*np.cos(np.pi/(4*BETA))))
    else:
        return (4 * BETA / np.pi / np.sqrt(bit_period) * \
            (np.cos((1 + BETA) * np.pi * t / bit_period) + \
             (1 - BETA) * np.pi / (4 * BETA) * np.sinc((1-BETA)*t/bit_period)) / \
                (1 - (4*BETA*t/bit_period)**2))


def rrc(t):
    '''
    Input: T, evaluation point (seconds)
    Output: value of root-raised-cosine at time T
    '''
    # Delay between two bits
    bit_period = 1/BIT_FREQUENCY
    # Total amount of bits to transmit
    nb_bits = len(LIST_OF_BITS)
    # To be returned (sum of contributions)
    s = 0.0
    # Max value of rrc
    m = 4*BETA/np.pi/np.sqrt(bit_period) + (1-BETA)/np.sqrt(bit_period) + sum(abs(2*rootRaisedCosine(i*bit_period)) for i in range(1, TRUNCATION))

    if(t < - TRUNCATION * bit_period  or t >= (nb_bits + TRUNCATION) * bit_period):
        # T out of support
        r = 0.0
    else:
        # Bits that will affect function at time T
        relevant_bits = np.zeros(2*TRUNCATION+1)
        for i in range(2*TRUNCATION+1):
            j = t/bit_period + i - TRUNCATION
            j = int(j) if int(j) <= j else int(j) - 1
            if(j >= 0 and j < nb_bits):
                relevant_bits[i] = -1 if LIST_OF_BITS[j] == '0' else 1

        for i in range(2*TRUNCATION+1):
            tt = t/bit_period
            tt = t - int(tt)*bit_period if int(tt) <= tt else t - (int(tt)-1)*bit_period
            if(t == bit_period * (1 / 4 / BETA + (i - TRUNCATION))):
                # L'Hospital's rule because of potential discontinuity
                s += relevant_bits[i] * BETA / np.pi / np.sqrt(2*bit_period) * 1 / m * \
                     ((np.pi + 2) * np.sin(np.pi/4/BETA) + \
                      (np.pi - 2) * np.cos(np.pi/4/BETA))
            else:
                # General case formula
                s += relevant_bits[i] * 4*BETA/np.pi/np.sqrt(bit_period) * 1 / m * \
                     (np.cos((1 + BETA) * np.pi * ((tt / bit_period - (i-TRUNCATION)))) + \
                      (1 - BETA) * np.pi / 4 / BETA * \
                      np.sinc((1 - BETA) * (tt / bit_period - (i-TRUNCATION))))/ \
                      (1 - (4*BETA*(tt / bit_period - (i-TRUNCATION)))**2)

    return s

###   ###   ###   ###   ###   ###   ###

if(WAVEFORM_TYPE == 'sinus'):
    f = sin
elif(WAVEFORM_TYPE == 'rectangle'):
    f = step
elif(WAVEFORM_TYPE == 'rrc'):
    f = rrc
