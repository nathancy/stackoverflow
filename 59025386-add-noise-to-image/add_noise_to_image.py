import cv2
import numpy as np
from skimage.util import random_noise
 
# Load the image
image = cv2.imread('1.png', 0)
 
# Add salt-and-pepper noise to the image
noise = random_noise(image, mode='s&p', amount=0.011)
 
# The above function returns a floating-point image in the range [0, 1]
# so need to change it to 'uint8' with range [0,255]
noise = np.array(255 * noise, dtype=np.uint8)
 
cv2.imshow('noise',noise)
cv2.imwrite('noise.png',noise)
cv2.waitKey()
