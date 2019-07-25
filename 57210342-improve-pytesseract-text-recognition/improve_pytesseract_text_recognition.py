import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

image = cv2.imread('1.png',0)
thresh = cv2.threshold(image, 220, 255, cv2.THRESH_BINARY)[1]

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

result = 255 - close
result = cv2.GaussianBlur(result, (3,3), 0)
cv2.imshow('thresh', thresh)
cv2.imshow('close', close)
cv2.imshow('result', result)

print(pytesseract.image_to_string(result))
cv2.waitKey()
