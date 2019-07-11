import cv2
import numpy as np

image = cv2.imread('1.jpg')
mask = np.zeros(image.shape, np.uint8)
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray,100,200)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
close = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel)
minLineLength = 10
maxLineGap = 350
lines = cv2.HoughLinesP(close,1,np.pi/180,100,minLineLength,maxLineGap)
for line in lines:
    for x1,y1,x2,y2 in line:
        cv2.line(mask,(x1,y1),(x2,y2),(255,255,255),3)

mask = cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)
cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

for c in cnts:
    cv2.drawContours(image, [c], -1, (255,255,255), -1)

cv2.imshow('mask', mask)
cv2.imshow('image', image)
cv2.imwrite('image.png', image)
cv2.waitKey()
