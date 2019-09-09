import cv2
import numpy as np

image = cv2.imread('1.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
mask = np.zeros(image.shape, dtype=np.uint8)

cnts = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

cv2.fillPoly(mask, cnts, [255,255,255])
mask = 255 - mask
result = cv2.bitwise_or(image, mask)

cv2.imshow('mask', mask)
cv2.imshow('result', result)
cv2.waitKey(0)
