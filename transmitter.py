#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy as np
import cv2

from config import TRUNCATURE, BIT_PERIOD
from time import time
from t_waveform_former import f


def transmit(f):
    '''
    Input: function of time, F: R+ -> [0, 1]
    Opens window and sends F in bw
    '''
    beginning = time()

    cv2.namedWindow('frame')

    while(time() < beginning + 5.0):
        img = np.full((512, 512, 3), np.array([0, 255, 0]), dtype="uint8")
        cv2.imshow('frame', img)
        cv2.waitKey(1)


    # Ramp for calibration
    time_mark = time()
    while(time() < time_mark + 2):
        value = (time() - time_mark)*0.5*255
        img = np.full((512, 512, 3), np.array([value, value, value]), dtype="uint8")
        cv2.imshow('frame', img)
        cv2.waitKey(1)

    start_signal = time()

    while(True):
        t = time() - start_signal - TRUNCATURE/BIT_PERIOD
        img = np.full((512, 512), (f(t)+1)/2.0)

        # Display the frame
        cv2.imshow('frame', img)

        # Break if ESC is pressed
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()


transmit(f)
