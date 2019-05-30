import cv2

original_image = cv2.imread('1.png')
original_copy = original_image.copy()
image = cv2.imread('2.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray, 130, 255, 1)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
dilate = cv2.dilate(canny, kernel, iterations=1)

cnts = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.01 * peri, True)
    x,y,w,h = cv2.boundingRect(approx)
    aspect_ratio = w / float(h)

    if (aspect_ratio >= 0.8 and aspect_ratio <= 1.6):
        ROI = original_copy[y:y+h, x:x+w]
        cv2.rectangle(original_image,(x,y),(x+w,y+h),(0,255,0),3)

cv2.imshow('canny', canny)
cv2.imshow('dilate', dilate)
cv2.imshow('original image', original_image)
cv2.imshow('ROI', ROI)
cv2.waitKey(0)


