#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy as np
import cv2

from time import time
from waveform_former import f


def transmit(f):
    '''
    Input: function of time, F: R+ -> [0, 1]
    Opens window and sends F in bw
    '''
    beginning = time()

    while(True):
        cv2.namedWindow('frame')

        t = time() - beginning
        img = np.full((512, 512), f(t))

        # Display the frame
        cv2.imshow('frame', img)

        # Break if ESC is pressed
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()

transmit(f)
