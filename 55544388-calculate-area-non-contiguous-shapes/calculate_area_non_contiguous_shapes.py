import cv2
import numpy

def grab_contours(cnts):
    # OpenCV v2.4, v4-official
    if len(cnts) == 2:
        return cnts[0]
    # OpenCV v3
    elif len(cnts) == 3:
        return cnts[1]

image = cv2.imread("test.png")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edged = cv2.Canny(gray, 120, 255, 1)
cv2.imshow("canny", edged)

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
cnts = grab_contours(cnts)

contour_image = edged.copy()
area = 0

for c in cnts:
    area += cv2.contourArea(c) 
    cv2.drawContours(contour_image,[c], 0, (100,5,10), 3)

print(area)
cv2.putText(contour_image, str(area), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100,255,100), 2)
cv2.imshow("area", contour_image)
cv2.waitKey(0)
