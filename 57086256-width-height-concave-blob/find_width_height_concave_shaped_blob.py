import cv2
import numpy as np

image = cv2.imread('1.png')
inverted = 255 - image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = 255 - gray

cnts = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

for c in cnts:
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    cv2.circle(inverted, (cX, cY), 5, (36, 255, 12), -1)
    inverted[cY][:] = (36, 255, 12)
    inverted[:, cX] = (36, 255, 12)
    row_pixels = cv2.countNonZero(gray[cY][:])
    column_pixels = cv2.countNonZero(gray[:, cX])

print('row', row_pixels)
print('column', column_pixels)
cv2.imshow('inverted', inverted)
cv2.imwrite('inverted.png', image)
cv2.waitKey(0)
