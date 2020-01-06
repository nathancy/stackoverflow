import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load image, create mask, grayscale, Otsu's threshold
image = cv2.imread('1.png')
mask = np.zeros(image.shape, dtype=np.uint8)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Filter for ROI using contour area and aspect ratio
cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    area = cv2.contourArea(c)
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.05 * peri, True)
    x,y,w,h = cv2.boundingRect(approx)
    aspect_ratio = w / float(h)
    if area > 2000 and aspect_ratio > .5:
        mask[y:y+h, x:x+w] = image[y:y+h, x:x+w]

# Perfrom OCR with Pytesseract
data = pytesseract.image_to_string(mask, lang='eng', config='--psm 6')
print(data)

cv2.imshow('thresh', thresh)
cv2.imshow('mask', mask)
cv2.waitKey()
