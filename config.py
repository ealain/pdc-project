# -*- coding: utf-8 -*-

import numpy as np

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

INPUT_FILE = 'input.txt'
EXCHANGE_FILE_PATH = './log'

# Available choices are 'ascii'
CODING_METHOD = 'ascii'

# Available choices are 'sinus', 'rectangle', 'rrc'
WAVEFORM_TYPE = 'rrc'
TRUNCATION = 10
BETA = 0.5

TRANSMITTER_COLOR = [50, 125, 46]

BIT_FREQUENCY = 12.0
SAMPLING_FREQUENCY = 30.0

# Lower and upper bounds of color detection for screen detection
# These colors are in the BGR format
# It is configured here to detect green
SCREEN_DETECTION_LOWER = np.array([0, 120, 0], dtype="uint8")
SCREEN_DETECTION_UPPER = np.array([120, 255, 120], dtype="uint8")

ALLOWED_DETECTION_TIME = 2.0  # (Seconds)
# Approx. 90 15' screens 3m away
VALID_MIN_AREA = 0.0
VALID_MAX_AREA = SCREEN_WIDTH * SCREEN_HEIGHT / 60.0
VALID_AREA_RATIO = 0.8
