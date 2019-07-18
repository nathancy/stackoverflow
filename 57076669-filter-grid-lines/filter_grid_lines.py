import cv2
import numpy as np

image = cv2.imread('1.png',0)
blur = cv2.GaussianBlur(image, (5,5), 0)
thresh = cv2.threshold(blur, 130, 255, cv2.THRESH_BINARY_INV)[1]

vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,5))
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,1))
remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel)
remove_vertical = cv2.morphologyEx(remove_horizontal, cv2.MORPH_OPEN, horizontal_kernel)

cnts = cv2.findContours(remove_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

mask = np.ones(image.shape, dtype=np.uint8)
for c in cnts:
    area = cv2.contourArea(c)
    if area > 50:
        cv2.drawContours(mask, [c], -1, (255,255,255), -1)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
mask = cv2.dilate(mask, kernel, iterations=1)
image = 255 - image
result = 255 - cv2.bitwise_and(mask, image)

cv2.imshow('result', result)
cv2.imwrite('result.png', result)
cv2.imshow('mask', mask)
cv2.waitKey(0)
