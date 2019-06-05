import cv2
import numpy as np

original_image = cv2.imread('1.png')
image = original_image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
dilate = cv2.dilate(thresh, kernel, iterations=5)

# Find contours
cnts = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

# Create a blank white mask
mask = np.zeros(image.shape, dtype='uint8')
mask.fill(255)

# Iterate thorugh contours and filter for ROI
for c in cnts:
    area = cv2.contourArea(c)
    if area < 15000:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
        mask[y:y+h, x:x+w] = original_image[y:y+h, x:x+w]

cv2.imshow("mask", mask)
cv2.imshow("image", image)
cv2.imshow("dilate", dilate)
cv2.imshow("thresh", thresh)
cv2.imshow("result", image)
cv2.waitKey(0)
