import cv2
import numpy as np

# Load image, grayscale, Otsu's threshold
image = cv2.imread('1.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Filter using contour hierarchy
cnts, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
hierarchy = hierarchy[0]
for component in zip(cnts, hierarchy):
    currentContour = component[0]
    currentHierarchy = component[1]
    x,y,w,h = cv2.boundingRect(currentContour)
    # Has inner contours which means it is unfilled
    if currentHierarchy[3] > 0:
        cv2.putText(image, 'Unfilled', (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (36,255,12), 2)
    # No child which means it is filled
    elif currentHierarchy[2] == -1:
        cv2.putText(image, 'Filled', (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (36,255,12), 2)

cv2.imshow('image', image)
cv2.waitKey()
