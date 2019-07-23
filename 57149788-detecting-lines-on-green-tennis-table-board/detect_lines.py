import cv2

image = cv2.imread('1.jpg')
image = cv2.resize(image, (960, 1024))
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (7,7), 0)
canny = cv2.Canny(blur, 120, 255, 1)

vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,9))
remove_horizontal = cv2.morphologyEx(canny, cv2.MORPH_OPEN, vertical_kernel)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
dilate = cv2.morphologyEx(remove_horizontal, cv2.MORPH_CLOSE, kernel)

cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

for c in cnts:
    area = cv2.contourArea(c)
    if area > 50:
        cv2.drawContours(image, [c], -1, (36,255,12), 3)

cv2.imwrite('result.png', image)
cv2.imwrite('canny.png', canny)
cv2.imwrite('remove_horizontal.png', remove_horizontal)
cv2.waitKey()
