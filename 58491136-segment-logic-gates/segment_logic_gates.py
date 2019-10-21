import cv2
import numpy as np

# Grayscale + Otsu's threshold
image = cv2.imread('1.jpg')
original = image.copy()
mask = np.zeros(image.shape, dtype=np.uint8)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Find lines
minLineLength = 10
maxLineGap = 150
lines = cv2.HoughLinesP(thresh,1,np.pi/180,100,minLineLength,maxLineGap)
for line in lines:
    for x1,y1,x2,y2 in line:
        cv2.line(thresh,(x1,y1),(x2,y2),(0,0,0),5)

# Morphological operations to clean image
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9,9))
close  = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=3)
cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

# Contour filtering and ROI extraction
ROI_number = 0
for c in cnts:
    area = cv2.contourArea(c)
    if area > 3000:
        x,y,w,h = cv2.boundingRect(c)
        ROI = original[y:y+h,x:x+w]
        cv2.imwrite('ROI_{}.png'.format(ROI_number), ROI)
        cv2.rectangle(image, (x, y), (x+w, y+h), (36, 255, 12), 8)
        ROI_number += 1

cv2.imwrite('thresh.png', thresh)
cv2.imwrite('close.png', close)
cv2.imwrite('image.png', image)
