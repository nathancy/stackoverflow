import numpy as np
import cv2

image = cv2.imread('1.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.merge([gray, gray, gray])
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower = np.array([35, 90, 88])
upper = np.array([179, 255, 255])
mask = cv2.inRange(hsv, lower, upper)
colored_output = cv2.bitwise_and(image, image, mask=mask)
gray_output = cv2.bitwise_and(gray, gray, mask=255-mask)
result = cv2.add(colored_output, gray_output)

cv2.imshow('colored_output', colored_output)
cv2.imshow('gray_output', gray_output)
cv2.imshow('result', result)
cv2.waitKey()
