import cv2
import numpy as np
from matplotlib import pyplot as plt

image = cv2.imread('1.jpg')

alpha = 1.95 # Contrast control (1.0-3.0)
beta = 0 # Brightness control (0-100)

manual_result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

cv2.imshow('original', image)
cv2.imshow('manual_result', manual_result)
cv2.waitKey()
