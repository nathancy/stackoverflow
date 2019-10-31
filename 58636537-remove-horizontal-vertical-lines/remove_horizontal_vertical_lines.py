import cv2

image = cv2.imread('1.png')

kernel_vertical = cv2.getStructuringElement(cv2.MORPH_RECT, (1,50))
temp1 = 255 - cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel_vertical)

horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50,1))
temp2 = 255 - cv2.morphologyEx(image, cv2.MORPH_CLOSE, horizontal_kernel)

temp3 = cv2.add(temp1, temp2)
result = cv2.add(temp3, image)

cv2.imshow('result', result)
cv2.waitKey()
