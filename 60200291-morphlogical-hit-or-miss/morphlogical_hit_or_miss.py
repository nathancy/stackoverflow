import cv2
import numpy as np

# Load image, grayscale, Otsu's threshold
image = cv2.imread('1.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Perform morphological hit or miss operation
kernel = np.array([[-1,-1,-1], [-1,1,-1], [-1,-1,-1]])
dot_mask = cv2.filter2D(thresh, -1, kernel)

# Bitwise-xor mask with binary image to remove dots
result = cv2.bitwise_xor(thresh, dot_mask)

# Dilate to fix damaged text pixels
# since the text quality has decreased from thresholding
# then bitwise-and with input image
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
dilate = cv2.dilate(result, kernel, iterations=1)
result = cv2.bitwise_and(image, image, mask=dilate)
result[dilate==0] = [255,255,255]

cv2.imshow('dot_mask', dot_mask)
cv2.imshow('thresh', thresh)
cv2.imshow('result', result)
cv2.imshow('dilate', dilate)
cv2.waitKey()
