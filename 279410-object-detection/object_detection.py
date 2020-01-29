import cv2
import numpy as np

# Load image, convert to grayscale, and Otsu's threshold 
image = cv2.imread('1.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Find contours and extract the bounding rectangle coordintes
# then find moments to obtain the centroid
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    # Obtain bounding box coordinates and draw rectangle
    x,y,w,h = cv2.boundingRect(c)
    cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)

    # Find center coordinate and draw center point
    M = cv2.moments(c)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    cv2.circle(image, (cx, cy), 2, (36,255,12), -1)
    print('Center: ({}, {})'.format(cx,cy))

cv2.imshow('image', image)
cv2.waitKey()
