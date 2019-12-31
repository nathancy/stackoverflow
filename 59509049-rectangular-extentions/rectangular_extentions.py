import cv2

# Load image, convert to grayscale, Otsu's threshold
image = cv2.imread('1.png')
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Create kernel and morph close 
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
close = 255 - cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=5)

# Find contours and filter using contour area
cnts = cv2.findContours(close, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    area = cv2.contourArea(c)
    if area > 100 and area < 25000:
        cv2.drawContours(image, [c], -1, (36,255,12), 4)

cv2.imshow('thresh', thresh)
cv2.imshow('close', close)
cv2.imshow('image', image)
cv2.waitKey()
