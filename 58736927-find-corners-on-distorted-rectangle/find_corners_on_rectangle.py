import cv2
import numpy as np
import imutils

# Resize image, blur, and Otsu's threshold
image = cv2.imread('1.png')
resize = imutils.resize(image, width=500)
mask = np.zeros(resize.shape, dtype=np.uint8)
gray = cv2.cvtColor(resize, cv2.COLOR_BGR2GRAY)
blur = cv2.bilateralFilter(gray,9,75,75)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Find distorted rectangle contour and draw onto a mask
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
rect = cv2.minAreaRect(cnts[0])
box = cv2.boxPoints(rect)
box = np.int0(box)
cv2.drawContours(resize,[box],0,(36,255,12),2)
cv2.fillPoly(mask, [box], (255,255,255))

# Find corners on the mask
mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
corners = cv2.goodFeaturesToTrack(mask, maxCorners=4, qualityLevel=0.5, minDistance=150)

for corner in corners:
    x,y = corner.ravel()
    cv2.circle(resize,(x,y),8,(155,20,255),-1)
    print("({}, {})".format(x,y))

cv2.imshow('resize', resize)
cv2.imshow('thresh', thresh)
cv2.imshow('mask', mask)
cv2.waitKey()
