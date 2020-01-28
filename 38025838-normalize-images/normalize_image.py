import cv2
import numpy as np

# Load image as grayscale and crop ROI
image = cv2.imread('1.png', 0)
x, y, w, h = 364, 633, 791, 273
ROI = image[y:y+h, x:x+w]

# Calculate mean and STD
mean, STD  = cv2.meanStdDev(ROI)

# Clip frame to lower and upper STD
offset = 0.2
clipped = np.clip(image, mean - offset*STD, mean + offset*STD).astype(np.uint8)

# Normalize to range
result = cv2.normalize(clipped, clipped, 0, 255, norm_type=cv2.NORM_MINMAX)

cv2.imshow('image', image)
cv2.imshow('ROI', ROI)
cv2.imshow('result', result)
cv2.waitKey()
