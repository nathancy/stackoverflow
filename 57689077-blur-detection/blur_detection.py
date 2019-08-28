import cv2
import numpy as np

image = cv2.imread('1.jpg')

result = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
dilate = cv2.dilate(thresh, kernel, iterations=3)

cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

ROI_num = 0
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    ROI = image[y:y+h, x:x+w]
    value = cv2.Laplacian(ROI, cv2.CV_64F).var()  
    cv2.rectangle(result, (x, y), (x + w, y + h), (36,255,12), 2)
    cv2.putText(result, "{0:.2f}".format(value), (x,y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (36,255,12), 2)
    cv2.imshow("ROI_{}".format(ROI_num), ROI)
    ROI_num += 1
    
    print('ROI_Number: {}, Value: {}'.format(ROI_num, value))

cv2.imshow('thresh', thresh)
cv2.imshow('dilate', dilate)
cv2.imshow('result', result)
cv2.waitKey(0)
