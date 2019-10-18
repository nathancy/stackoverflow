import cv2
import numpy as np

image = cv2.imread('1.png')
mask = np.ones(image.shape, dtype=np.uint8) * 255
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (7,7), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    area = cv2.contourArea(c)
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.05 * peri, True)
    if len(approx) == 4 and area > 500:
        x,y,w,h = cv2.boundingRect(approx)
        mask[y:y+h, x:x+w] = image[y:y+h, x:x+w]

# Remove horizontal lines
mask = cv2.cvtColor(255 - mask, cv2.COLOR_BGR2GRAY)
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (55,3))
detect_horizontal = cv2.morphologyEx(mask, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
cnts = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    cv2.drawContours(mask, [c], -1, (0,0,0), 9)

# Remove vertical lines
vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,30))
detect_vertical = cv2.morphologyEx(mask, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
cnts = cv2.findContours(detect_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    cv2.drawContours(mask, [c], -1, (0,0,0), 9)

# Bitwise mask with input image
result = cv2.bitwise_and(image, image, mask=mask)
result[mask==0] = (255,255,255)

cv2.imshow('mask', mask)
cv2.imshow('thresh', thresh)
cv2.imshow('result', result)
cv2.waitKey()
