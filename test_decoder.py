#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from t_waveform_former import rrc
from r_tuple_former import formTuples, rootRaisedCosine
from r_decoder import decode
from r_tuple_former import low_pass_filter
from r_tuple_former import correlation_function
from r_decoder import sequence_to_char


import matplotlib.pyplot as plt
import numpy as np

f = np.vectorize(rrc)

t = np.arange(-4, 15, 0.001)
print(t)
signal = f(t)
plt.plot(t, signal)
plt.show()


receivedSignal = []
for i in range(int(len(signal)/33.33333)):
    receivedSignal.append(signal[int(33.33333*i)])

rrcSignal = [rootRaisedCosine(x) for x in np.arange(-10*1.0/3.0, 10*1.0/3.0, 1.0/30.0)]

plt.plot(np.arange(-10/3.0, 10/3.0, 1.0/30.0), rrcSignal)
plt.show()

print(len(receivedSignal))
print(formTuples(receivedSignal))
print(sequence_to_char(formTuples(receivedSignal)))

corr = correlation_function(receivedSignal)
print(len(corr))
plt.plot(corr)
plt.show()
print(corr[0::100])

if(False): # test for correlation
    beta = 0.5
    truncation = 10
    bit_period = 1.0 / 3.0
    t = np.arange(-truncation * bit_period, truncation * bit_period, 1.0 / (30.0*10))
    filter = [rootRaisedCosine(x) for x in t]
    for i in range(10):
        plt.plot(t[i:len(t):10], [rootRaisedCosine(x) for x in t[i:len(t):10]])
        plt.show()



if(False): # test of low pass filtering
    x = [(np.cos(2*np.pi*30*a) + np.cos(2*np.pi*5*a)) for a in np.arange(0, 1, 1/100.0)]
    y = low_pass_filter(x, 5, 20, 100)
    plt.plot(np.arange(0, 1, 1/100.0), y)
    plt.plot(np.arange(0, 1, 1/100.0), x)
    plt.show()


