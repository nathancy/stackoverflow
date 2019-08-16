import cv2
import numpy as np

image = cv2.imread('1.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
sharpen = cv2.filter2D(gray, -1, sharpen_kernel)

cv2.imwrite('sharpen.png', sharpen)
sharpen = 255 - sharpen
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
dilate = cv2.dilate(sharpen, kernel, iterations=1)

result = 255 - dilate
cv2.imwrite('result.png', result)
cv2.waitKey(0)

