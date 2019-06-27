import cv2
import numpy as np

image = cv2.imread('2.png')

blur = cv2.GaussianBlur(image, (3,3), 0)
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

thresh = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY_INV)[1]

cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
c = max(cnts, key=cv2.contourArea)

left = tuple(c[c[:, :, 0].argmin()][0])
right = tuple(c[c[:, :, 0].argmax()][0])
top = tuple(c[c[:, :, 1].argmin()][0])
bottom = tuple(c[c[:, :, 1].argmax()][0])

cv2.drawContours(image, [c], -1, (36, 255, 12), 2)
cv2.circle(image, left, 8, (0, 50, 255), -1)
cv2.circle(image, right, 8, (0, 255, 255), -1)
cv2.circle(image, top, 8, (255, 50, 0), -1)
cv2.circle(image, bottom, 8, (255, 255, 0), -1)

print('left: {}'.format(left))
print('right: {}'.format(right))
print('top: {}'.format(top))
print('bottom: {}'.format(bottom))
cv2.imshow('thresh', thresh)
cv2.imshow('image', image)
cv2.waitKey()

