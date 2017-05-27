#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from t_waveform_former import rrc
from r_tuple_former import formTuples, rootRaisedCosine
from r_decoder import decode
from r_tuple_former import low_pass_filter


import matplotlib.pyplot as plt
import numpy as np

f = np.vectorize(rrc)

t = np.arange(-0.5, 4.5, 0.001)
print(t)
signal = f(t)
plt.plot(t, signal)
plt.show()


receivedSignal = []
for i in range(int(len(signal)/33.33333)):
    receivedSignal.append(signal[int(33.33333*i)])

rrcSignal = [rootRaisedCosine(x) for x in np.arange(-10*1.0/20.0, 10*1.0/20.0, 1.0/30.0)]

plt.plot(np.arange(-10/20.0, 10/20.0, 1.0/30.0), rrcSignal)
plt.show()

print(formTuples(receivedSignal))
print(decode(formTuples(receivedSignal)))

if(True):
    x = [(np.cos(2*np.pi*30*a) + np.cos(2*np.pi*5*a)) for a in np.arange(0, 1, 1/100.0)]
    y = low_pass_filter(x, 5, 20, 100)
    plt.plot(np.arange(0, 1, 1/100.0), y)
    plt.plot(np.arange(0, 1, 1/100.0), x)
    plt.show()


