from skimage.transform import (hough_line, hough_line_peaks)
import numpy as np
import cv2

image = cv2.imread('2.png')

# Compute arithmetic mean
image = np.mean(image, axis=2)

# Perform Hough Transformation to detect lines
hspace, angles, distances = hough_line(image)

# Find angle
angle=[]
for _, a , distances in zip(*hough_line_peaks(hspace, angles, distances)):
    angle.append(a)

# Obtain angle for each line
angles = [a*180/np.pi for a in angle]

# Compute difference between the two lines
angle_difference = np.max(angles) - np.min(angles)
print(angle_difference)
