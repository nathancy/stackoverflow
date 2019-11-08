import numpy as np
import cv2

# Read image, create blank masks, color threshold
image = cv2.imread('1.jpg')
blank_mask = np.zeros(image.shape, dtype=np.uint8)
original = image.copy()
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower = np.array([0, 18, 0])
upper = np.array([88, 255, 139])
mask = cv2.inRange(hsv, lower, upper)

# Perform morphological operations
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=1)

# Find contours and filter for largest contour
# Draw largest contour onto a blank mask then bitwise-and
cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
cv2.fillPoly(blank_mask, [cnts], (255,255,255))
blank_mask = cv2.cvtColor(blank_mask, cv2.COLOR_BGR2GRAY)
result = cv2.bitwise_and(original,original,mask=blank_mask)

# Crop ROI from result
x,y,w,h = cv2.boundingRect(blank_mask)
ROI = result[y:y+h, x:x+w]

cv2.imshow('result', result)
cv2.imshow('ROI', ROI)
cv2.waitKey()
