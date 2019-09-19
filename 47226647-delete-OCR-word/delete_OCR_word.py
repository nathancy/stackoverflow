import cv2
import pytesseract

words_to_remove = ['on', 'you', 'crazy', 'diamond']
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

image = cv2.imread("1.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
inverted_thresh = 255 - thresh
dilate = cv2.dilate(inverted_thresh, kernel, iterations=4)

cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    ROI = thresh[y:y+h, x:x+w]
    data = pytesseract.image_to_string(ROI, lang='eng',config='--psm 6').lower()
    if data in words_to_remove:
        image[y:y+h, x:x+w] = [255,255,255]

cv2.imshow("thresh", thresh)
cv2.imshow("dilate", dilate)
cv2.imshow("image", image)
cv2.waitKey(0)

