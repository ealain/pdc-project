#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from config import EXCHANGE_FILE_PATH
from r_tuple_former import formTuples
import matplotlib.pyplot as plt
import sys


def ascii_to_char(l):
    '''
    :param l: list of bits you want to translate into characters
    :return: list of corresponding characters (ascii)
    '''

    l = l[0: int(len(l)/8)*8]
    asciiList = []
    for i in range(len(l)/8):
        asciiList.append(l[i*8:i*8+8])
    charList = []
    for c in asciiList:
        asciiCode = 0
        for b in c:
            asciiCode = asciiCode*2 + b
        charList.append(chr(asciiCode))

    return charList


def sequence_to_char(l):
    '''
    :param l: list of "tuples" from the tuple former
    :return: corresponding text
    '''
    bits = []
    for k in l:
        if(k>=0):
            bits.append(1)
        else:
            bits.append(0)

    return ascii_to_char(bits)


def calibrate_value(min_value, max_value, value):
    return (value - min_value) / (max_value - min_value) * 2.0 - 1.0

def calibrate_ramp(ramp, value):
    for (i, x) in enumerate(ramp):
        if x == value or (x > value and i == 0):
            return float(i) / len(ramp)
        elif x > value:
            xprec = ramp[i-1]
            a = x - xprec
            b = x - a * float(i)
            return (value - b) / a / len(ramp)
    return float(len(ramp)-1) / len(ramp)


def decode(debug=False):
    f = open(EXCHANGE_FILE_PATH)
    value_prec = -1

    # Calibration
    calib = False
    green = True
    ramp = []

    # Measure
    values = []
    measuring = False

    line = f.readline()
    while len(line) > 0:
        value = float(line.strip())
        if green:
            if value_prec != -1:
                if value < value_prec * 80.0 / 100.0:
                    green = False
                    calib = True
                    value = 0.0
        elif calib:
            if value < value_prec * 90.0 / 100.0:
                calib = False
            else:
                ramp.append(value)
        else:
            values.append(calibrate_value(0.0, 1.0, calibrate_ramp(ramp, value)))
        value_prec = value
        line = f.readline()

    f.close()

    tuples = formTuples(values)
    chars = sequence_to_char(tuples)

    if debug:
        print(min(ramp))
        print(max(ramp))
        print(ramp)
        print values
        print len(values)

        plt.plot(values)
        print(tuples)
        plt.show()

    print(chars)

    f = open("result.txt", "w")
    f.write("".join(chars))
    f.close()


if __name__ == "__main__":
    debug = False
    if len(sys.argv) > 1 and sys.argv[1] == "debug":
        debug = True
    decode(debug)
