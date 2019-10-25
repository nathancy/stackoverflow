import cv2
import numpy as np

image = cv2.imread("1.png")
original = image.copy()
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

hsv_lower = np.array([0,150,50])
hsv_upper = np.array([10,255,255])
mask = cv2.inRange(hsv, hsv_lower, hsv_upper)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=1)

cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
offset = 20
ROI_number = 0
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    cv2.rectangle(image, (x - offset, y - offset), (x + w + offset, y + h + offset), (36,255,12), 2)
    ROI = original[y-offset:y+h+offset, x-offset:x+w+offset]

    cv2.imwrite('ROI_{}.png'.format(ROI_number), ROI)
    ROI_number += 1

cv2.imshow('mask', mask)
cv2.imshow('close', close)
cv2.imshow('image', image)
cv2.waitKey()

