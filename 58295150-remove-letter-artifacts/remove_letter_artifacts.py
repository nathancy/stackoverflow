import cv2
import numpy as np

# Read in image, convert to grayscale, and Otsu's threshold
image = cv2.imread('1.png')
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Create special horizontal kernel and dilate 
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (70,1))
dilate = cv2.dilate(thresh, horizontal_kernel, iterations=1)

# Detect horizontal lines, sort for largest contour, and draw on mask
mask = np.zeros(image.shape, dtype=np.uint8)
detected_lines = cv2.morphologyEx(dilate, cv2.MORPH_OPEN, horizontal_kernel, iterations=1)
cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
for c in cnts:
    cv2.drawContours(mask, [c], -1, (255,255,255), -1)
    break

# Bitwise-and to get result and color background white
mask = cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)
result = cv2.bitwise_and(image,image,mask=mask)
result[mask==0] = (255,255,255)

cv2.imshow('thresh', thresh)
cv2.imshow('dilate', dilate)
cv2.imshow('result', result)
cv2.waitKey()

