import cv2
import numpy as np

image = cv2.imread('2.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,3)

mask = thresh.copy()
mask = cv2.merge([mask,mask,mask])

picture_threshold = image.shape[0] * image.shape[1] * .05
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    area = cv2.contourArea(c)
    if area < picture_threshold:
        cv2.drawContours(mask, [c], -1, (0,0,0), -1)

mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
result = cv2.bitwise_xor(thresh, mask)

text_pixels = cv2.countNonZero(result)
percentage = (text_pixels / (image.shape[0] * image.shape[1])) * 100
print('Percentage: {:.2f}%'.format(percentage))

cv2.imshow('thresh', thresh)
cv2.imshow('result', result)
cv2.imshow('mask', mask)
cv2.waitKey()
