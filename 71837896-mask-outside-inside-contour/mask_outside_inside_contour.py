import numpy as np
import cv2
from scipy import interpolate

# Load image, make blank mask, define rough contour points
image = cv2.imread('1.jpg')
mask = np.zeros(image.shape, dtype=np.uint8) 
x = np.array([192, 225, 531, 900, 500])
y = np.array([154, 281, 665, 821, 37])
x = np.r_[x, x[0]]
y = np.r_[y, y[0]]

# Smooth contours
tck, u = interpolate.splprep([x, y], s=0, per=True)
x_new, y_new = interpolate.splev(np.linspace(0, 1, 1000), tck)
smooth_contour = np.array([[[int(i[0]), int(i[1])]] for i in zip(x_new, y_new)])

# Draw contour onto blank mask in white
cv2.drawContours(mask, [smooth_contour], 0, (255,255,255), -1)
result1 = cv2.bitwise_and(image, mask)
result2 = cv2.bitwise_and(image, 255 - mask)

cv2.imshow('image', image)
cv2.imshow('mask', mask)
cv2.imshow('result1', result1)
cv2.imshow('result2', result2)
cv2.waitKey()
