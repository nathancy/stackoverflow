import numpy as np
from imutils import contours
import cv2

# Load image, grayscale, Gaussian blur, Otsu's threshold
image = cv2.imread('1.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Find contours and remove text inside cells
cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    area = cv2.contourArea(c)
    if area < 4000:
        cv2.drawContours(thresh, [c], -1, 0, -1)

# Invert image
invert = 255 - thresh
offset, old_cY, first = 10, 0, True
visualize = cv2.cvtColor(invert, cv2.COLOR_GRAY2BGR)

# Find contours, sort from top-to-bottom and then sum up column/rows
cnts = cv2.findContours(invert, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
(cnts, _) = contours.sort_contours(cnts, method="top-to-bottom")
for c in cnts:
    # Find centroid
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    
    # New row
    if (abs(cY) - abs(old_cY)) > offset:
        if first:
            row, table = [], []
            first = False
        old_cY = cY
        table.append(row)
        row = []
    
    # Cell in same row
    if ((abs(cY) - abs(old_cY)) <= offset) or first:
        row.append(1)
   
    # Uncomment to visualize 
    '''
    cv2.circle(visualize, (cX, cY), 10, (36, 255, 12), -1) 
    cv2.imshow('visualize', visualize)
    cv2.waitKey(200)
    '''

print('Rows: {}'.format(len(table)))
print('Columns: {}'.format(len(table[1])))

cv2.imshow('invert', invert)
cv2.imshow('thresh', thresh)
cv2.waitKey()
