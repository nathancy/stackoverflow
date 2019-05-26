import cv2

image = cv2.imread("1.PNG")
thresh = cv2.threshold(image, 115, 255, cv2.THRESH_BINARY_INV)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
dilate = cv2.dilate(thresh, kernel, iterations=1)
final = cv2.threshold(dilate, 115, 255, cv2.THRESH_BINARY_INV)[1]

cv2.imshow('image', image)
cv2.imshow('dilate', dilate)
cv2.imshow('final', final)
cv2.waitKey(0)
