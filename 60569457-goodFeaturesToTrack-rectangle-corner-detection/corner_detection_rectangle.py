import cv2

# Load image, grayscale, blur, Otsu's threshold
image = cv2.imread('1.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3,3), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Remove small noise with contour area filtering
cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    area = cv2.contourArea(c)
    if area < 150:
        cv2.drawContours(thresh, [c], -1, 0, -1)

# Find corners and draw onto image
corners = cv2.goodFeaturesToTrack(thresh,150,0.5,5)
for corner in corners:
    x,y = corner.ravel()
    cv2.circle(image,(x,y),3,(36,255,12),-1)

# The number of rectangles is corners / 4
print('Rectangles: {}'.format(len(corners)/4))

cv2.imshow('image', image)
cv2.waitKey()
