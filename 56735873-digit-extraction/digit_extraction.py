import cv2
import numpy as np
from imutils import contours

image = cv2.imread('1.png')
original = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray, 130, 255, 1)

vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,2))
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,1))
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
erode = cv2.erode(canny, vertical_kernel)
cv2.imshow('remove horizontal', erode)
dilate = cv2.dilate(erode, vertical_kernel, iterations=5)
cv2.imshow('dilate vertical', dilate)
erode = cv2.erode(dilate, horizontal_kernel, iterations=1)
cv2.imshow('remove vertical', erode)
dilate = cv2.dilate(erode, kernel, iterations=4)
cv2.imshow('dilate horizontal', dilate)

cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

digit_contours = []
for c in cnts:
    area = cv2.contourArea(c)
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.01 * peri, True)
    x,y,w,h = cv2.boundingRect(approx)
    aspect_ratio = w / float(h)
    
    if (aspect_ratio >= 0.4 and aspect_ratio <= 1.3):
        if area > 150:
            ROI = original[y:y+h, x:x+w]
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
            digit_contours.append(c)

sorted_digit_contours = contours.sort_contours(digit_contours, method='left-to-right')[0]
contour_number = 0
for c in sorted_digit_contours:
    x,y,w,h = cv2.boundingRect(c)
    ROI = original[y:y+h, x:x+w]
    cv2.imwrite('ROI_{}.png'.format(contour_number), ROI)
    contour_number += 1

cv2.imshow('canny', canny)
cv2.imshow('image', image)
cv2.waitKey(0)


