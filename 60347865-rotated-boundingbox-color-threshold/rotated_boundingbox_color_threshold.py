import cv2
import numpy as np

# Load image, convert to HSV, color threshold to get mask
image = cv2.imread('1.png')
original = image.copy()
blank = np.zeros(image.shape[:2], dtype=np.uint8)
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower = np.array([0, 0, 0])
upper = np.array([179, 255, 165])
mask = cv2.inRange(hsv, lower, upper)

# Merge text into a single contour
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
close = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=3)

# Find contours
cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    # Filter using contour area and aspect ratio
    x,y,w,h = cv2.boundingRect(c)
    area = cv2.contourArea(c)
    ar = w / float(h)
    if (ar > 1.4 and ar < 4) or ar < .85 and area > 100:
        # Find rotated bounding box
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(image,[box],0,(36,255,12),2)
        cv2.drawContours(blank,[box],0,(255,255,255),-1)

# Bitwise operations to isolate text
extract = cv2.bitwise_and(mask, blank)
extract = cv2.bitwise_and(original, original, mask=extract)
extract[extract==0] = 255

cv2.imshow('mask', mask)
cv2.imshow('image', image)
cv2.imshow('close', close)
cv2.imshow('extract', extract)
cv2.waitKey()
