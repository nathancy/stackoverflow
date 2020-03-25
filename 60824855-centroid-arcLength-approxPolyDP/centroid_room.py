import cv2
import numpy as np

# Load image, grayscale, Otsu's threshold
image = cv2.imread('1.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Remove text
cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    area = cv2.contourArea(c)
    if area < 1000:
        cv2.drawContours(thresh, [c], -1, 0, -1)

thresh = 255 - thresh
result = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
coordinates = []

# Find rectangular boxes and obtain centroid coordinates
cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    area = cv2.contourArea(c)
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.05 * peri, True)
    if len(approx) == 4 and area < 100000:
        # cv2.drawContours(result, [c], -1, (36,255,12), 1)
        M = cv2.moments(c)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        coordinates.append((cx, cy))
        cv2.circle(result, (cx, cy), 3, (36,255,12), -1)
        cv2.putText(result, '({}, {})'.format(int(cx), int(cy)), (int(cx) -40, int(cy) -10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36,255,12), 2)

print(coordinates)
cv2.imshow('thresh', thresh)
cv2.imshow('image', image)
cv2.imshow('result', result)
cv2.waitKey()
