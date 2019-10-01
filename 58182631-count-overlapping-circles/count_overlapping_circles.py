import cv2
import numpy as np
import math

image = cv2.imread('1.jpg')
black_box = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Count overlapping circles
single_area = 375
overlapping = 0

cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    area = cv2.contourArea(c)
    blob_area = math.ceil(area/single_area)
    if blob_area > 1:
        overlapping += blob_area
        cv2.drawContours(image, [c], -1, (36,255,12), 2)

# Find circles touching image boundary
h, w, _ = image.shape
boundary = 10
touching = 0
box = np.array(([boundary,boundary], 
                      [w-boundary,boundary], 
                      [w-boundary, h-boundary], 
                      [boundary, h-boundary]))
cv2.fillPoly(black_box, [box], [0,0,0])

copy = black_box.copy()
copy = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)
copy = cv2.threshold(copy, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

cnts = cv2.findContours(copy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    area = cv2.contourArea(c)
    if area > 100:
        touching += 1
        cv2.drawContours(black_box, [c], -1, (36,255,12), 2)

print('Overlapping:', overlapping)
print('Touching:', touching)
cv2.imshow('image', image)
cv2.imshow('black_box', black_box)
cv2.waitKey()
