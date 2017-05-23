#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy as np
import cv2

from config import SCREEN_DETECTION_LOWER, SCREEN_DETECTION_UPPER

def detect_color(frame):
    return cv2.inRange(frame, SCREEN_DETECTION_LOWER, SCREEN_DETECTION_UPPER)

def detect_screen(frame):
    filtered_frame = detect_color(frame)
    cv2.imshow('filtered_frame', filtered_frame)
    contours = cv2.findContours(filtered_frame, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)
    print contours
    return contours


def main():
    cap = cv2.VideoCapture(0)
    while(True):
        ret, frame = cap.read()

        contours = detect_screen(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
