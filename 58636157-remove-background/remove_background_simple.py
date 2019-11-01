import cv2
import numpy as np

image = cv2.imread('1.jpg')

image[np.where((image > [0,0,105]).all(axis=2))] = [255,255,255]

cv2.imshow('image', image)
cv2.waitKey()
