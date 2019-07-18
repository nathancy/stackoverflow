import cv2
import numpy as np

image = cv2.imread('1.png', 0)
sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
sharpen = cv2.filter2D(image, -1, sharpen_kernel)
thresh = cv2.threshold(sharpen,220, 255,cv2.THRESH_BINARY)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)
result = cv2.dilate(opening, kernel, iterations=3)

cv2.imshow('thresh', thresh)
cv2.imshow('sharpen', sharpen)
cv2.imshow('opening', opening)
cv2.imshow('result', result)
cv2.waitKey() 
