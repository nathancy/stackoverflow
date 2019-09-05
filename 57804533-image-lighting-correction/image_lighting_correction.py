import cv2

image = cv2.imread('1.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5), 0)
thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
         cv2.THRESH_BINARY_INV,9,11)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
dilate = cv2.dilate(close, kernel, iterations=1)
result = 255 - dilate 

cv2.imshow('thresh', thresh)
cv2.imshow('close', close)
cv2.imshow('dilate', dilate)
cv2.imshow('result', result)
cv2.waitKey()
