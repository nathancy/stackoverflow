import cv2

image = cv2.imread('1.jpg', 0)
blur = cv2.medianBlur(image, 9)
thresh = cv2.threshold(blur, 25, 255, cv2.THRESH_BINARY)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)
close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=3)
canny = cv2.Canny(close, 120, 255, 1)

cv2.imshow('canny', canny)
cv2.imwrite('blur.png', blur)
cv2.imwrite('blur.png', blur)
cv2.imwrite('blur.png', blur)
cv2.waitKey()
