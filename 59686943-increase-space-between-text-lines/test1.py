import cv2
import numpy as np 
from imutils import contours

# Load image, grayscale, blur, Otsu's threshold
image = cv2.imread('1.png')
original = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3,3), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
invert = 255 - thresh  
height, width = image.shape[:2]

# Dilate with a horizontal kernel to connect text contours
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,2))
dilate = cv2.dilate(thresh, kernel, iterations=2)

# Extract each line contour
lines = []
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
(cnts, _) = contours.sort_contours(cnts, method="top-to-bottom")
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    cv2.rectangle(image, (0, y), (width, y+h), (36,255,12), 2)
    line = original[y:y+h, 0:width]
    line = cv2.cvtColor(line, cv2.COLOR_BGR2GRAY)
    lines.append(line)

# Append white space in between each line
space = np.ones((1, width), dtype=np.uint8) * 255
result = np.zeros((0, width), dtype=np.uint8)
result = np.concatenate((result, space), axis=0)
for line in lines:
    result = np.concatenate((result, line), axis=0)
    result = np.concatenate((result, space), axis=0)

cv2.imshow('result', result)
cv2.imshow('image', image)
cv2.imshow('dilate', dilate)
cv2.waitKey()
