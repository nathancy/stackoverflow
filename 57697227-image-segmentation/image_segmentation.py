import numpy as np
import cv2

image = cv2.imread('1.jpg')
result = image.copy()
image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower = np.array([0,0,200])
upper = np.array([179, 77, 255])
mask = cv2.inRange(image, lower, upper)
result = cv2.bitwise_and(result,result, mask=mask)

cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

for c in cnts:
    area = cv2.contourArea(c)
    if area < 1:
        cv2.drawContours(result, [c], -1, (0,0,0), -1)

cv2.imshow('mask', mask)
cv2.imshow('result', result)
cv2.waitKey()
