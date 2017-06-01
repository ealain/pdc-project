# -*- coding: utf-8 -*-

import numpy as np

INPUT_FILE = 'alphabet.txt'
EXCHANGE_FILE_PATH = './log'

# Available choices are 'ascii'
CODING_METHOD = 'ascii'

# Available choices are 'sinus', 'rectangle', 'rrc'
WAVEFORM_TYPE = 'rrc'
TRUNCATURE = 10
BETA = 0.5

BIT_FREQUENCY = 14.0
SAMPLING_FREQUENCY = 30.0

# Lower and upper bounds of color detection for screen detection
# These colors are in the BGR format
# It is configured here to detect green
SCREEN_DETECTION_LOWER = np.array([0, 120, 0], dtype="uint8")
SCREEN_DETECTION_UPPER = np.array([120, 255, 120], dtype="uint8")
