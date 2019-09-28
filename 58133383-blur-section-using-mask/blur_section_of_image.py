import cv2

image = cv2.imread('1.png')
mask = cv2.imread('mask.png')
mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    ROI = image[y:y+h, x:x+w]
    image[y:y+h, x:x+w] = cv2.GaussianBlur(ROI, (41,41), 0)

cv2.imshow('image', image)
cv2.imshow('ROI', ROI)
cv2.waitKey()
