#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy as np
import cv2

from config import SCREEN_DETECTION_LOWER, SCREEN_DETECTION_UPPER

def detect_color(frame):
    """Return a mask of the frame according to the color defined in config.py
    """
    return cv2.inRange(frame, SCREEN_DETECTION_LOWER, SCREEN_DETECTION_UPPER)

def detect_screen(frame, mask):
    """Return the frame filtered with the given mask
    """
    frame_screen = cv2.bitwise_and(frame, frame, mask=mask)
    return frame_screen

def get_screen_gray_level(frame_screen):
    """Return the average gray level of the non-black parts of `frame_screen`
    """
    avg = 0.0
    c = 0
    gray_frame_screen = cv2.cvtColor(frame_screen, cv2.COLOR_BGR2GRAY)
    for x in gray_frame_screen:
        for y in x:
            if y > 0:
                avg += y
                c += 1
    return float(avg) / float(c)


def main():
    cap = cv2.VideoCapture(0)
    while(True):
        ret, frame = cap.read()

        mask = detect_color(frame)
        cv2.imshow('frame', frame)
        cv2.imshow('mask', mask)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    frame_screen = detect_screen(frame, mask)
    print get_screen_gray_level(frame_screen)
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
