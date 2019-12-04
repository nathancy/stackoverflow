import cv2

# Load image, grayscale, and Otsu's threshold
image = cv2.imread('1.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Remove large lines
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    area = w * h
    if area > 550:
        cv2.drawContours(thresh, [c], -1, (0,0,0), -1)

# Dilate with vertical kernel to connect characters
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,5))
dilate = cv2.dilate(thresh, kernel, iterations=2)

# Remove small noise
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    area = cv2.contourArea(c)
    if area < 150:
        cv2.drawContours(dilate, [c], -1, (0,0,0), -1)

# Bitwise mask with input image
result = cv2.bitwise_and(image, image, mask=dilate)
result[dilate==0] = (255,255,255)

cv2.imshow('dilate', dilate)
cv2.imshow('result', result)
cv2.imshow('thresh', thresh)
cv2.waitKey()
