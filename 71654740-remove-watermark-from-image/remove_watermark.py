import numpy as np
import cv2

# Load image, convert to HSV, then HSV color threshold
image = cv2.imread('1.jpg')
original = image.copy()
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower = np.array([0, 0, 0])
upper = np.array([179, 255, 163])
mask = cv2.inRange(hsv, lower, upper)

# Dilate to repair
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
dilate = cv2.dilate(mask, kernel, iterations=1)

# Second pass of HSV to remove pink
colored = cv2.bitwise_and(original, original, mask=dilate)
colored_hsv = cv2.cvtColor(colored, cv2.COLOR_BGR2HSV)
lower_two = np.array([96, 89, 161])
upper_two = np.array([179, 255, 255])
mask_two = cv2.inRange(colored_hsv, lower_two, upper_two)

# Convert to grayscale then remove pink contours
result = cv2.cvtColor(colored, cv2.COLOR_BGR2GRAY)
result[result <= 10] = 255
cv2.imshow('result before removal', result)
result[mask_two==255] = 255

cv2.imshow('dilate', dilate)
cv2.imshow('colored', colored)
cv2.imshow('mask_two', mask_two)
cv2.imshow('result after removal', result)
cv2.waitKey()
