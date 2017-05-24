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
    bit_period = 1.0/SAMPLING_FREQUENCY*(1+beta)

    if (t== bit_period/(4*beta)):
        return (beta/(np.pi*np.sqrt(2*bit_period)) * \
                ((np.pi + 2)*np.sin(np.pi/(4*beta)) + (np.pi - 2)*np.cos(np.pi/(4*beta))))
    else:
        return (4 * beta / np.pi / np.sqrt(bit_period) * \
            (np.cos((1 + beta) * np.pi * t / bit_period) + \
             (1 - beta) * np.pi / (4 * beta) * np.sinc((1-beta)*t/bit_period)) / \
                (1 - (4*beta*t/bit_period)**2))


def formTuples(signal):
    '''
    Input: signal: Signal sampled at frequency Te
    Output: List of corresponding symbols ( in {-1, 1} )
    '''

    # signal must be sampled at 2*Fe
    signal = resample(signal)

    beta = 0.5
    truncation = 10
    bit_period = 1.0/SAMPLING_FREQUENCY*(1+beta)
    t = np.arange(-truncation*bit_period, truncation*bit_period, 0.5/SAMPLING_FREQUENCY)
    m = 4*beta/np.pi/np.sqrt(bit_period) + (1-beta)/np.sqrt(bit_period) + sum(abs(2*rootRaisedCosine(i*bit_period)) for i in range(1, truncation))

    # the filter must be sampled at 2*Fe
    filter = [rootRaisedCosine(x) for x in t]

    tupleList = []

    i = 0
    while(len(signal)- int(i*(bit_period*2*SAMPLING_FREQUENCY)) >= len(filter)):
        s = 0
        for j in range(len(filter)):
            s += signal[int(i*(bit_period*2*SAMPLING_FREQUENCY)) + j] * m * filter[j] / (2.0 * SAMPLING_FREQUENCY)
        tupleList.append(s)
        i = i+1

    return tupleList
