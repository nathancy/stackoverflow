import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

image = cv2.imread('2.jpg',0)
thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV)[1]

result = cv2.GaussianBlur(thresh, (5,5), 0)
result = 255 - result

data = pytesseract.image_to_string(result, lang='eng',config='--psm 6')
print(data)

cv2.imshow('thresh', thresh)
cv2.imshow('result', result)
cv2.waitKey()
