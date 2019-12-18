import cv2
import numpy as np

# Load image, bilaterial blur, and Otsu's threshold
image = cv2.imread('1.png')
mask = np.zeros(image.shape, dtype=np.uint8)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.bilateralFilter(gray,9,75,75)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Perform morpholgical operations
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,10))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=1)

# Find distorted rectangle contour and draw onto a mask
cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
rect = cv2.minAreaRect(cnts[0])
box = cv2.boxPoints(rect)
box = np.int0(box)
cv2.drawContours(image,[box],0,(36,255,12),4)
cv2.fillPoly(mask, [box], (255,255,255))

# Find corners
mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
corners = cv2.goodFeaturesToTrack(mask,4,.8,100)
offset = 25
for corner in corners:
    x,y = corner.ravel()
    cv2.circle(image,(x,y),5,(36,255,12),-1)
    x, y = int(x), int(y)
    cv2.rectangle(image, (x - offset, y - offset), (x + offset, y + offset), (36,255,12), 3)
    print("({}, {})".format(x,y))

cv2.imshow('image', image)
cv2.imshow('thresh', thresh)
cv2.imshow('close', close)
cv2.imshow('mask', mask)
cv2.waitKey()
