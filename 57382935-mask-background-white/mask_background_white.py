import numpy as np
import cv2

image = cv2.imread('new.png')
result = image.copy()
image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower = np.array([90, 38, 0])
upper = np.array([145, 255, 255])
mask = cv2.inRange(image, lower, upper)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
close = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)

cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

result[close==0] = (255,255,255)

dilate = cv2.dilate(close, kernel, iterations=2)

cv2.imshow('result', result)
cv2.imshow('dilate', dilate)
cv2.imshow('close', close)
cv2.waitKey()
