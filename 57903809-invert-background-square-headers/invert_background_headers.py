import cv2

image = cv2.imread('1.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3,3), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.015 * peri, True)
    area = cv2.contourArea(c)
    if len(approx) == 4 and area > 1000:
        x,y,w,h = cv2.boundingRect(c)
        ROI = 255 - image[y:y+h,x:x+w]
        image[y:y+h, x:x+w] = ROI

cv2.imshow('image', image)
cv2.waitKey()
