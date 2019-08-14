import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

image = cv2.imread('2.png')
original = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = 255 - gray

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
dilate = cv2.dilate(gray, kernel, iterations=4)

cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

image_number = 0
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    ROI = original[y:y+h, x:x+w]
    data = pytesseract.image_to_string(ROI, lang='eng', config='--psm 10')
    if data.isdigit():
        print('Page #: ', data)
        cv2.imwrite("ROI_{}.png".format(image_number), ROI)
        image_number += 1
    
cv2.imshow('gray', gray)
cv2.imshow('dilate', dilate)
cv2.imshow('original', original)
cv2.waitKey()
