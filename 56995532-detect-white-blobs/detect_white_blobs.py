import cv2

image = cv2.imread('1.png')

blur = cv2.medianBlur(image, 5)
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray,180,255, cv2.THRESH_BINARY)[1]

cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

min_area = 50
white_dots = []
for c in cnts:
    area = cv2.contourArea(c)
    if area > min_area:
        cv2.drawContours(image, [c], -1, (36, 255, 12), 2)
        white_dots.append(c)

print(len(white_dots))
cv2.imshow('thresh', thresh)
cv2.imshow('image', image)
cv2.imwrite('image.png', image)
cv2.waitKey()

