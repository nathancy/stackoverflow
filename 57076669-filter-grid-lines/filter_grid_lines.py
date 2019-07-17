import cv2
import numpy as np

image = cv2.imread('1.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.medianBlur(gray, 15)

thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,3)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
erode = cv2.erode(thresh, kernel, iterations=1)
dilate = cv2.dilate(erode, kernel, iterations=3)

cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

mask = np.zeros(image.shape, dtype=np.uint8)
for c in cnts:
    area = cv2.contourArea(c)
    if area > 850:
        cv2.drawContours(mask, [c], -1, (255,255,255), -1)

mask = cv2.dilate(mask, kernel, iterations=1)
image = 255 - image
result = 255 - cv2.bitwise_and(mask, image)

cv2.imshow('result', result)
cv2.waitKey(0)
exit(1)
