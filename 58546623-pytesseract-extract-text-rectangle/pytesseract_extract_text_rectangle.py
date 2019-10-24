import cv2
import pytesseract
import imutils

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Resize, grayscale, Otsu's threshold
image = cv2.imread('1.png')
image = imutils.resize(image, width=500)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Invert image and perform morphological operations
inverted = 255 - thresh
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15,3))
close = cv2.morphologyEx(inverted, cv2.MORPH_CLOSE, kernel, iterations=1)

# Find contours and filter using aspect ratio and area
cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    area = cv2.contourArea(c)
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.01 * peri, True)
    x,y,w,h = cv2.boundingRect(approx)
    aspect_ratio = w / float(h)
    if (aspect_ratio >= 2.5 or area < 75):
        cv2.drawContours(thresh, [c], -1, (255,255,255), -1)

# Blur and perform text extraction
thresh = cv2.GaussianBlur(thresh, (3,3), 0)
data = pytesseract.image_to_string(thresh, lang='eng',config='--psm 6')
print(data)

cv2.imshow('close', close)
cv2.imshow('thresh', thresh)
cv2.waitKey()
