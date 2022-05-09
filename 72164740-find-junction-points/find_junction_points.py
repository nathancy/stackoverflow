import cv2

# Load image, grayscale, Gaussian blur, Otsus threshold
image = cv2.imread('1.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3,3), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Find horizonal lines
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,1))
horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=1)

# Find vertical lines
vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,5))
vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=1)

# Find joint intersections then the centroid of each joint
joints = cv2.bitwise_and(horizontal, vertical)
cnts = cv2.findContours(joints, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    # Find centroid and draw center point
    x,y,w,h = cv2.boundingRect(c)
    centroid, coord, area = cv2.minAreaRect(c)
    cx, cy = int(centroid[0]), int(centroid[1])
    cv2.circle(image, (cx, cy), 5, (36,255,12), -1)

cv2.imshow('thresh', thresh)
cv2.imshow('joints', joints)
cv2.imshow('horizontal', horizontal)
cv2.imshow('vertical', vertical)
cv2.imshow('image', image)
cv2.waitKey()     
