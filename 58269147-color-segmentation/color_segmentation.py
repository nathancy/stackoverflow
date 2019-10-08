import numpy as np
import cv2

# Color threshold
image = cv2.imread('1.jpg')
original = image.copy()
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower = np.array([0, 31, 182])
upper = np.array([57, 75, 209])
mask = cv2.inRange(hsv, lower, upper)
result = cv2.bitwise_and(original,original,mask=mask)

# Find floor contour on mask
cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    cv2.drawContours(original,[c], -1, (36,255,12), 2)

cv2.imshow('mask', mask)
cv2.imshow('result', result)
cv2.imshow('original', original)
cv2.waitKey()
