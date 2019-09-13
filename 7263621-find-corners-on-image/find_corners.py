import cv2

image = cv2.imread('1.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray, 120, 255, 1)

corners = cv2.goodFeaturesToTrack(canny,4,0.5,50)

for corner in corners:
    x,y = corner.ravel()
    cv2.circle(image,(x,y),5,(36,255,12),-1)

cv2.imshow('canny', canny)
cv2.imshow('image', image)
cv2.waitKey()
