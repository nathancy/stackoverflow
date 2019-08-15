import numpy as np
import cv2

image = cv2.imread('1.png')
result = image.copy()
image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower = np.array([21,0,0])
upper = np.array([179, 255, 209])
mask = cv2.inRange(image, lower, upper)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2))
close = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)

result[close==0] = (0,0,0)

cv2.imshow('cleaned', result)

retouch_mask = (result <= [250.,250.,250.]).all(axis=2)
result[retouch_mask] = [0,0,0]

cv2.imshow('mask', mask)
cv2.imshow('close', close)
cv2.imshow('result', result)
cv2.waitKey()
