import cv2
import numpy as np
import pytesseract
from imutils import contours
import imutils

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load image, enlarge, convert to grayscale, Otsu's threshold
image = cv2.imread('1.png')
image = imutils.resize(image, width=1000)
height, width = image.shape[:2]
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Remove horizontal lines
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50,1))
detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
cnts = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    cv2.drawContours(thresh, [c], -1, 0, -1)

# Remove vertical lines
vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,50))
detect_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
cnts = cv2.findContours(detect_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    cv2.drawContours(thresh, [c], -1, 0, -1)

# Morph close to combine adjacent contours into a single contour
invoice_data = []
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (85,5))
close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=3)

# Find contours, sort from top-to-bottom
# Iterate through contours, extract row ROI, OCR, and parse data
cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
(cnts, _) = contours.sort_contours(cnts, method="top-to-bottom")

row = 0
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    ROI = image[y:y+h, 0:width]
    ROI = cv2.GaussianBlur(ROI, (3,3), 0)
    data = pytesseract.image_to_string(ROI, lang='eng', config='--psm 6')
    parsed = [word.lower() for word in data.split()] 
    if 'tariff' in parsed or 'number' in parsed:
        row_data = {}
        row_data['line'] = str(row)
        row_data['tariff'] = parsed[-1]
        row_data['quantity'] = parsed[2]
        row_data['amount'] = str(max(parsed[10], parsed[11]))
        row += 1

        print(row_data)
        invoice_data.append(row_data)
        
        # Visualize row extraction
        '''
        mask = np.zeros(image.shape, dtype=np.uint8)
        cv2.rectangle(mask, (0, y), (width, y + h), (255,255,255), -1)
        display_row = cv2.bitwise_and(image, mask)

        cv2.imshow('ROI', ROI)
        cv2.imshow('display_row', display_row)
        cv2.waitKey(1000)
        '''
print(invoice_data)
cv2.imshow('thresh', thresh)
cv2.imshow('close', close)
cv2.waitKey()
