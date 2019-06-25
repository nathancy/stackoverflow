import cv2

image = cv2.imread('1.jpg')
blur = cv2.medianBlur(image, 9)
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 110 ,255, cv2.THRESH_BINARY_INV)[1]

cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

min_area = 5000
for c in cnts:
    area = cv2.contourArea(c)
    if area > min_area:
        cv2.drawContours(image,[c], 0, (36,255,12), 2)

cv2.imshow('thresh', thresh)
cv2.imshow('image', image)
cv2.waitKey(0)
