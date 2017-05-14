import numpy as np
import cv2

from time import time
from waveform_former import f

beginning = time()

while(True):
    cv2.namedWindow('frame')    

    t = time() - beginning
    img = np.full((512, 512), f(t))

    # Display the frame
    cv2.imshow('frame', img)
    
    # Break if ESC is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
