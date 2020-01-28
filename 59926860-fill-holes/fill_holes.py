import cv2
import numpy as np

# Load image, create mask, grayscale, and Otsu's threshold
image = cv2.imread('2.png')
mask = np.zeros(image.shape, dtype=np.uint8)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Perform morph operations
open_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, open_kernel, iterations=1)
close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, close_kernel, iterations=3)

# Find horizontal sections and draw rectangle on mask 
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25,3))
detect_horizontal = cv2.morphologyEx(close, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
cnts = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    cv2.rectangle(mask, (x, y), (x + w, y + h), (255,255,255), -1)
    cv2.rectangle(mask, (x, y), (x + w, y + h), (255,255,255), 2)

# Find vertical sections and draw rectangle on mask 
vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,25))
detect_vertical = cv2.morphologyEx(close, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
cnts = cv2.findContours(detect_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    cv2.rectangle(mask, (x, y), (x + w, y + h), (255,255,255), -1)
    cv2.rectangle(mask, (x, y), (x + w, y + h), (255,255,255), 2)

# Color mask onto original image
mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
image[mask==255] = [0,0,0]

cv2.imshow('opening', opening)
cv2.imshow('close', close)
cv2.imshow('image', image)
cv2.imshow('thresh', thresh)
cv2.imshow('mask', mask)
cv2.waitKey()

