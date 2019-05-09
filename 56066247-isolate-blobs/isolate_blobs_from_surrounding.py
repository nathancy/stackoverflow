import numpy as np
import cv2

original_image = cv2.imread("1.jpg")
image = original_image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
thresh = cv2.threshold(blurred, 110, 255,cv2.THRESH_BINARY)[1]
canny = cv2.Canny(thresh, 150, 255, 1)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
dilate = cv2.dilate(canny, kernel, iterations=1)

cv2.imshow("dilate", dilate)
cv2.imshow("thresh", thresh)
cv2.imshow("canny", canny)

# Find contours in the image
cnts = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

contours = []

threshold_min_area = 1100
threshold_max_area = 1200

for c in cnts:
    area = cv2.contourArea(c)
    if area > threshold_min_area and area < threshold_max_area:
        cv2.drawContours(original_image,[c], 0, (0,255,0), 3)
        contours.append(c)

cv2.imshow("detected", original_image) 
print('contours detected: {}'.format(len(contours)))
cv2.waitKey(0)
