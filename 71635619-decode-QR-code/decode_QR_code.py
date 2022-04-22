import cv2
from pyzbar.pyzbar import decode

# Load image, grayscale, Gaussian blur, Otsu's threshold 
image = cv2.imread('1.png')
original = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3,3), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Dilate to combine contours
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
dilate = cv2.dilate(thresh, kernel, iterations=2)

# Find contours and extract ROI
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    ROI = original[y:y+h, x:x+w]
    cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3)

# Decode QR code
data = decode(ROI)
print(data)

cv2.imshow('thresh', thresh)
cv2.imshow('dilate', dilate)
cv2.imshow('image', image)
cv2.imshow('ROI', ROI)
cv2.waitKey()
