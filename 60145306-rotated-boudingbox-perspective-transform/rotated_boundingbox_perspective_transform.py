import cv2
import pytesseract
import numpy as np
from imutils.perspective import four_point_transform

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load image, convert to HSV, color threshold to get mask
image = cv2.imread('1.png')
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower = np.array([0, 0, 0])
upper = np.array([100, 175, 110])
mask = cv2.inRange(hsv, lower, upper)

# Morph close to connect individual text into a single contour
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
close = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=3)

# Find rotated bounding box then perspective transform
cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
rect = cv2.minAreaRect(cnts[0])
box = cv2.boxPoints(rect)
box = np.int0(box)
cv2.drawContours(image,[box],0,(36,255,12),2)
warped = four_point_transform(255 - mask, box.reshape(4, 2))

# OCR
data = pytesseract.image_to_string(warped, lang='eng', config='--psm 6')
print(data)

cv2.imshow('mask', mask)
cv2.imshow('close', close)
cv2.imshow('warped', warped)
cv2.imshow('image', image)
cv2.waitKey()
