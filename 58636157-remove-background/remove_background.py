import cv2

image = cv2.imread('1.jpg')

# Remove vertical and horizontal lines
kernel_vertical = cv2.getStructuringElement(cv2.MORPH_RECT, (1,50))
temp1 = 255 - cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel_vertical)
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50,1))
temp2 = 255 - cv2.morphologyEx(image, cv2.MORPH_CLOSE, horizontal_kernel)
temp3 = cv2.add(temp1, temp2)
removed = cv2.add(temp3, image)

# Threshold and perform morphological operations
gray = cv2.cvtColor(removed, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)

# Filter using contour area and remove small noise
cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    area = cv2.contourArea(c)
    if area < 10:
        cv2.drawContours(close, [c], -1, (0,0,0), -1)

final = 255 - close 
cv2.imshow('removed', removed)
cv2.imshow('thresh', thresh)
cv2.imshow('close', close)
cv2.imshow('final', final)
cv2.imwrite('temp1.png', temp1)
cv2.imwrite('temp2.png', temp2)
cv2.imwrite('temp3.png', temp3)
cv2.waitKey()
