#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy as np
import cv2

from config import SCREEN_DETECTION_LOWER, SCREEN_DETECTION_UPPER


def detect_color(frame):
    """Return a mask of the frame according to the color defined in config.py
    """
    return cv2.inRange(frame, SCREEN_DETECTION_LOWER, SCREEN_DETECTION_UPPER)


def get_screen_gray_level(frame_screen):
    """Return the average gray level of the non-black parts of `frame_screen`
    """
    avg = 0.0
    c = 0
    gray_frame_screen = cv2.cvtColor(frame_screen, cv2.COLOR_BGR2GRAY)
    # Iteration over the lines
    for x in gray_frame_screen:
        # Iteration over the pixels
        for y in x:
            if y > 0:
                avg += y
                c += 1
    return float(avg) / float(c)


def screen_position():
    '''
    Returns position of rectangle x,y,w,h if:
        - bounding rectangle is big enough (more than 0.2 % of total captured image)
        - contour's area is more than 70% of the area of the bounding rectangle
    '''
    cap = cv2.VideoCapture(0)
    nb_max_iterations = 10
    for it in range(nb_max_iterations):
        ret, frame = cap.read()
        mask = detect_color(frame)
        masked_frame = cv2.bitwise_and(frame, frame, mask=mask)
        imgray = cv2.cvtColor(masked_frame, cv2.COLOR_BGR2GRAY)
        contours, hierarchy = cv2.findContours(imgray,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        contours = sorted(contours, key=lambda x:len(x), reverse=True)
        i = 0
        max_area = 480*640
        # Approx. 90 15' screens 3m away
        valid_min_area = max_area/120.0/4.0
        valid_max_area = max_area/60.0
        while(i < len(contours)):
            x,y,w,h = cv2.boundingRect(contours[i])
            rect_cnt = np.array([[[x, y]], [[x+w, y]], [[x+w, y+h]], [[x, y+h]]], dtype=np.int32)
            rect_cnt_area = cv2.contourArea(rect_cnt)
            valid_area_ratio = 0.5
            if(cv2.contourArea(contours[i]) > 0.7 * rect_cnt_area and rect_cnt_area > valid_min_area):
                cap.release()
                return x,y,w,h
            else:
                i += 1
    cap.release()
    return None


def main():
    '''
    Test screen_position
    '''
    cap = cv2.VideoCapture(0)
    while(True):
        ret, frame = cap.read()
        mask = detect_color(frame)
        cv2.imshow('frame', frame)
        cv2.imshow('mask', mask)
        masked_frame = cv2.bitwise_and(frame, frame, mask=mask)
        imgray = cv2.cvtColor(masked_frame, cv2.COLOR_BGR2GRAY)
        contours, hierarchy = cv2.findContours(imgray,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        contours = sorted(contours, key=lambda x:len(x), reverse=True)
        i = 0
        max_area = 480*640
        # Approx. 90 15' screens 3m away
        valid_min_area = max_area/120.0/4.0
        valid_max_area = max_area/60.0
        while(i < len(contours)):
            x,y,w,h = cv2.boundingRect(contours[i])
            rect_cnt = np.array([[[x, y]], [[x+w, y]], [[x+w, y+h]], [[x, y+h]]], dtype=np.int32)
            rect_cnt_area = cv2.contourArea(rect_cnt)
            valid_area_ratio = 0.5
            if(cv2.contourArea(contours[i]) > 0.7 * rect_cnt_area and rect_cnt_area > valid_min_area):
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                break
            else:
                i += 1

        cv2.imshow('Contours', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    print(get_screen_gray_level(frame_screen))
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
