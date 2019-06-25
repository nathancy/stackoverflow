import cv2

image = cv2.imread('1.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
thresh = cv2.threshold(blurred, 240 ,255, cv2.THRESH_BINARY_INV)[1]
canny = cv2.Canny(thresh, 50, 255, 1)

cnts = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

for c in cnts:
    cv2.drawContours(image,[c], 0, (36,255,12), 2)

cv2.imshow('thresh', thresh)
cv2.imshow('canny', canny)
cv2.imshow('image', image)
cv2.imwrite('thresh.png', thresh)
cv2.imwrite('canny.png', canny)
cv2.imwrite('image.png', image)
cv2.waitKey(0)
