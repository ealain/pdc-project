#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy as np
import cv2
from config import BIT_FREQUENCY, SCREEN_HEIGHT, SCREEN_WIDTH

def display_green():
    cv2.namedWindow('frame')
    while(True):
        img = np.full((SCREEN_HEIGHT, SCREEN_WIDTH, 3), np.array([0, 255, 0]), dtype="uint8")
        cv2.imshow('frame', img)

        # Break if ESC is pressed
        if cv2.waitKey(1) & 0xFF == 27:
            break
    

if __name__ == "__main__":
    display_green()
