#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from t_waveform_former import rrc
from r_tuple_former import formTuples, rootRaisedCosine

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
