import numpy as np
import cv2
import imutils

original_image = cv2.imread("1.jpg")
original_image = imutils.resize(original_image, width=500)
image = original_image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
canny = cv2.Canny(blurred, 120, 255, 1)

cv2.imshow("canny", canny)

# Find contours in the image
cnts = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

contours = []

contour_image = canny.copy()
threshold_min_area = 400
for c in cnts:
    area = cv2.contourArea(c)
    if area > threshold_min_area:
        cv2.drawContours(original_image,[c], 0, (0,255,0), 3)
        contours.append(c)

cv2.imshow("detected", original_image) 
print('contours detected: {}'.format(len(contours)))
cv2.waitKey(0)
