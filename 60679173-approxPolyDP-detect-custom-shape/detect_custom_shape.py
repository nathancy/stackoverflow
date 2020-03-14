import cv2
import numpy as np

# Load image, grayscale, Gaussian blur, Otsus threshold
image = cv2.imread('1.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3,3), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Find contours
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)
    area = cv2.contourArea(c)
    # Filter using contour approximation and area filtering (Remove small noise)
    if len(approx) > 4 and len(approx) < 8 and area > 200:
        # This is the larger version
        if area >= 5500:
            print('Match')
        # Smaller version
        elif area < 5500:
            print('No Match')
        cv2.drawContours(image, [c], -1, (255,0,12), 3)

cv2.imshow('thresh', thresh)
cv2.imshow('image', image)
cv2.waitKey()     
