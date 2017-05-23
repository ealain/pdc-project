# -*- coding: utf-8 -*-

import numpy as np
from config import SAMPLING_FREQUENCY

def resample(signal):
    '''
    :param signal: Signal sampled at frequency Te
    :return: a 2*Te frequency sampled version of signal (method used: signal blocking)
    '''
    resampledSignal = np.zeros(len(signal)*2)
    for i in range(len(signal)):
        resampledSignal[2*i] = signal[i]
        resampledSignal[2*i + 1] = signal[i]
    return resampledSignal

def rootRaisedCosine(t):
    beta = 0.5
    trunc = 10
    bit_period = 1/SAMPLING_FREQUENCY*2/3

    if (t== SAMPLING_FREQUENCY/(4*beta)):
        return (beta/(np.pi*np.sqrt(2*SAMPLING_FREQUENCY)) * \
                ((np.pi + 2)*np.sin(np.pi/(4*beta)) + (np.pi - 2)*np.cos(np.pi/(4*beta))))
    else:
        return (4 * beta / np.pi / np.sqrt(SAMPLING_FREQUENCY) * \
            (np.cos((1 + beta) * np.pi * t / SAMPLING_FREQUENCY) + \
             (1 - beta) * np.pi / (4 * beta) * np.sinc((1-beta)*t/SAMPLING_FREQUENCY)) / \
                (1 - (4*beta*t/SAMPLING_FREQUENCY)**2))




def tuple_former(signal):
    '''
    Input: signal: Signal sampled at frequency Te
    Output: List of corresponding symbols ( in {-1, 1} )
    '''

    # signal must be sampled at 2*Fe
    signal = resample(signal)

    beta = 0.5
    trunc = 10
    bit_period = 1/SAMPLING_FREQUENCY*2/3
    t = np.arange(-trunc*bit_period, trunc*bit_period, 0.5/SAMPLING_FREQUENCY)

    # the filter must be sampled at 2*Fe
    filter = [rootRaisedCosine(x) for x in t]

    tupleList = []

    i = 0
    while(len(signal)- int(i*(bit_period*2*SAMPLING_FREQUENCY)) >= len(filter)):
        s = 0
        for j in range(len(filter)):
            s += signal[int(i*(bit_period*2*SAMPLING_FREQUENCY)) + j] * filter[j]
        tupleList.append(s)
        i = i+1

    return tupleList

