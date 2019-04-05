from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
import numpy

DIGITS_LOOKUP = {
    (1, 1, 1, 0, 1, 1, 1): 0,
    (0, 0, 1, 0, 0, 1, 0): 1,
    (1, 0, 1, 1, 1, 1, 0): 2,
    (1, 0, 1, 1, 0, 1, 1): 3,
    (0, 1, 1, 1, 0, 1, 0): 4,
    (1, 1, 0, 1, 0, 1, 1): 5,
    (1, 1, 0, 1, 1, 1, 1): 6,
    (1, 0, 1, 0, 0, 1, 0): 7,
    (1, 1, 1, 1, 1, 1, 1): 8,
    (1, 1, 1, 1, 0, 1, 1): 9
}

image = cv2.imread("test.jpg")

image = imutils.resize(image, height=100)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 120, 255, 1)
cv2.imshow("1", edged)

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
displayCnt = None

for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    if len(approx) == 4:
        displayCnt = approx
        break

warped = four_point_transform(gray, displayCnt.reshape(4, 2))

thresh = cv2.threshold(warped, 0, 255,
    cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
cv2.imshow("2", thresh)

digit_cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
digit_cnts = imutils.grab_contours(digit_cnts)

threshold_max_area = 25
threshold_min_area = 5
contour_image = thresh.copy()

for c in digit_cnts:
    (x,y,w,h) = cv2.boundingRect(c)
    area = cv2.contourArea(c) 
    if area < threshold_max_area and area > threshold_min_area:
        cv2.drawContours(contour_image,[c], 0, (100,5,10), 3)

cv2.imshow("detect decimal", contour_image)
cv2.waitKey(0)


