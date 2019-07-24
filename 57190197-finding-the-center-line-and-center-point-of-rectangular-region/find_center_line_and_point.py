import imutils
import cv2
import numpy as np

# load the image, convert it to grayscale, blur it slightly, and threshold it
image = cv2.imread('1.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)

# threshold the image, then perform a series of erosions + dilations to remove any small regions of noise
thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
thresh = cv2.erode(thresh, None, iterations=2)
thresh = cv2.dilate(thresh, None, iterations=2)

contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

# Find the index of the largest contour
areas = [cv2.contourArea(c) for c in contours]
max_index = np.argmax(areas)
cnt=contours[max_index]

x,y,w,h = cv2.boundingRect(cnt)
cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)

M = cv2.moments(cnt)

cX = int(M["m10"] / M["m00"])
cY = int(M["m01"] / M["m00"])

cv2.circle(image, (cX, cY), 5, (36, 255, 12), -1)

# To draw line you can use cv2.line or numpy slicing
cv2.line(image, (x + int(w/2), y), (x + int(w/2), y+h), (0, 0, 255), 3)
# image[int(cY - h/2):int(cY+h/2), cX] = (36, 255, 12)

# show the output image
cv2.imshow("Image", image)
cv2.imwrite("Image.png", image)
cv2.waitKey(0)
