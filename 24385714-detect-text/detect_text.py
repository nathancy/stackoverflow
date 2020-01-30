import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load image, convert to HSV format, define lower/upper ranges, and perform
# color segmentation to create a binary mask
image = cv2.imread('1.jpg')
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower = np.array([0, 0, 218])
upper = np.array([157, 54, 255])
mask = cv2.inRange(hsv, lower, upper)

# Create horizontal kernel and dilate to connect text characters
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,3))
dilate = cv2.dilate(mask, kernel, iterations=5)

# Find contours and filter using aspect ratio
# Remove non-text contours by filling in the contour
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    ar = w / float(h)
    if ar < 5:
        cv2.drawContours(dilate, [c], -1, (0,0,0), -1)

# Bitwise dilated image with mask, invert, then OCR
result = 255 - cv2.bitwise_and(dilate, mask)
data = pytesseract.image_to_string(result, lang='eng',config='--psm 6')
print(data)

cv2.imshow('mask', mask)
cv2.imshow('dilate', dilate)
cv2.imshow('result', result)
cv2.waitKey()
