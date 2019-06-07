import cv2
import numpy as np

original_frame = cv2.imread("1.jpg")
frame = original_frame.copy()

# pts - location of the 4 corners of the roi
pts = np.array([[6, 1425],[953, 20],[1934, 40], [2541,1340]])
(x,y,w,h) = cv2.boundingRect(pts)

pts = pts - pts.min(axis=0)
mask = np.zeros(original_frame.shape, np.uint8)
cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)
result = cv2.bitwise_and(original_frame, mask)
white_background = cv2.bitwise_not(mask)

cv2.imshow('white_background', white_background)
cv2.imshow('mask', mask)
cv2.imshow('result', result)
print(result.shape)
cv2.waitKey(0)

