import cv2
import numpy as np

# Load in image and create copy
image = cv2.imread('1.png')
original = image.copy()

# Gaussian blur and extract blue channel
blur = cv2.GaussianBlur(image, (3,3), 0)
blue = blur[:,:,0]

# Threshold image and erode to isolate gate contour
thresh = cv2.threshold(blue,135, 255, cv2.THRESH_BINARY_INV)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
erode = cv2.erode(thresh, kernel, iterations=4)

# Create a mask and find contours
mask = np.zeros(original.shape, dtype=np.uint8)
cnts = cv2.findContours(erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

# Filter for gate contour using area and draw onto mask
for c in cnts:
    area = cv2.contourArea(c)
    if area > 6000:
        cv2.drawContours(mask, [c], -1, (255,255,255), 2)

# Dilate to restore contour and mask it with original image
dilate = cv2.dilate(mask, kernel, iterations=7)
result = cv2.bitwise_and(original, dilate)

cv2.imshow('thresh', thresh)
cv2.imshow('erode', erode)
cv2.imshow('mask', mask)
cv2.imshow('dilate', dilate)
cv2.imshow('result', result)
cv2.waitKey()
