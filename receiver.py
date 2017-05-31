#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy as np
import cv2, cv
from time import time
from sys import stdin

from config import SAMPLING_FREQUENCY, EXCHANGE_FILE_PATH
from r_screen_detect import screen_position

def receive():
    '''
    1. Locate screen
    2. Follow the variations of intensity in the screen
    '''
    sampling_period = 1/SAMPLING_FREQUENCY
    f = open(EXCHANGE_FILE_PATH, 'w')
    f.write('')
    x,y,w,h = screen_position()
    if((x,y,w,h) == (-1,-1,-1,-1)):
        print("Unable to detect screen")
        return
    cap = cv2.VideoCapture(0)
    last_written = -1.0
    while(True):
        last_read = time()
        ret, frame = cap.read()
        sub_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)[y:y+h, x:x+w]
        if(last_read - last_written >= sampling_period):
            last_written = time()
            f.write(str(np.mean(sub_frame))+'\n')


if __name__ == "__main__":
    receive()