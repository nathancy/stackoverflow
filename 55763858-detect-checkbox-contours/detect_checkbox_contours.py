import numpy as np
import imutils, cv2

original_image = cv2.imread("1.jpg")
image = original_image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 120, 255, 1)

cv2.imshow("edged", edged)

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

checkbox_contours = []

threshold_max_area = 250
threshold_min_area = 200
contour_image = edged.copy()

for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.035 * peri, True)
    (x, y, w, h) = cv2.boundingRect(approx)
    aspect_ratio = w / float(h)
    area = cv2.contourArea(c) 
    if area < threshold_max_area and area > threshold_min_area and (aspect_ratio >= 0.9 and aspect_ratio <= 1.1):
        cv2.drawContours(original_image,[c], 0, (0,255,0), 3)
        checkbox_contours.append(c)

print('checkbox_contours', len(checkbox_contours))
cv2.imshow("checkboxes", original_image)
cv2.waitKey(0)
