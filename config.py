# -*- coding: utf-8 -*-

import numpy as np

INPUT_FILE = 'alphabet.txt'

# Available choices are 'ascii'
CODING_METHOD = 'ascii'

# Available choices are 'sinus', 'rectangle', 'rrc'
WAVEFORM_TYPE = 'rrc'

SAMPLING_FREQUENCY = 30.0

# Lower and upper bounds of color detection for screen detection
# These colors are in the BGR format
SCREEN_DETECTION_LOWER = np.array([100, 0, 0], dtype="uint8")
SCREEN_DETECTION_UPPER = np.array([255, 100, 100], dtype="uint8")
