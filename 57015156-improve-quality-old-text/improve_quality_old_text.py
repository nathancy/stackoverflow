import cv2
import numpy as np

image = cv2.imread('1.png', 0)
clahe = cv2.createCLAHE().apply(image)

sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
sharpen = cv2.filter2D(clahe, -1, sharpen_kernel)

thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

cv2.imshow('clahe', clahe)
cv2.imwrite('clahe.png', clahe)
cv2.imshow('sharpen', sharpen)
cv2.imwrite('sharpen.png', sharpen)
cv2.imshow('thresh', thresh)
cv2.imwrite('thresh.png', thresh)
cv2.waitKey()
