#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy as np
import cv2, cv
from time import time

from r_screen_detect import screen_position

def receive():
    '''
    1. Locate screen
    2. Follow the variations of intensity in the screen
    '''
    #x,y,w,h = screen_position()
    x,y,w,h = (200, 200, 40, 40)
    intensity = []
    cap = cv2.VideoCapture(0)
    while(True):
        ret, frame = cap.read()
        sub_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)[y:y+h, x:x+w]
        intensity.append(np.mean(sub_frame))
        print(intensity[-1])


if __name__ == "__main__":
    receive()
