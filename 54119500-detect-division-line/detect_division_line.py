import cv2
import numpy as np

image = cv2.imread('1.jpg')
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5), 0)

thresh = cv2.threshold(blur,190, 255,cv2.THRESH_BINARY_INV)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5,5))
dilate = cv2.dilate(thresh, kernel, iterations=1)

minLineLength = 10
maxLineGap = 200
lines = cv2.HoughLinesP(dilate,1,np.pi/180,100,minLineLength,maxLineGap)
for line in lines:
    for x1,y1,x2,y2 in line:
        cv2.line(image,(x1,y1),(x2,y2),(0,0,255),3)

cv2.imshow('image', image)
cv2.imshow('thresh', thresh)
cv2.waitKey()
