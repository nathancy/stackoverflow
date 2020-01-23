import cv2
import numpy as np

# Load image, convert to HSV, and color threshold
image = cv2.imread('1.png')
blank_mask = np.zeros(image.shape, dtype=np.uint8)
original = image.copy()
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower = np.array([0, 0, 109])
upper = np.array([179, 36, 255])
mask = cv2.inRange(hsv, lower, upper)

# Morph open to remove noise
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

# Find contours and sort for largest contour
cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

# Obtain rotated bounding box and draw onto a blank mask
rect = cv2.minAreaRect(cnts)
box = cv2.boxPoints(rect)
box = np.int0(box)
cv2.drawContours(image,[box],0,(36,255,12),3)
cv2.fillPoly(blank_mask, [box], (255,255,255))

# Bitwise-and mask with input image 
blank_mask = cv2.cvtColor(blank_mask, cv2.COLOR_BGR2GRAY)
result = cv2.bitwise_and(original, original, mask=blank_mask)
result[blank_mask==0] = (255,255,255) # Color background white

# Detect corners
corners = cv2.goodFeaturesToTrack(blank_mask, maxCorners=4, qualityLevel=0.5, minDistance=150)
for corner in corners:
    x,y = corner.ravel()
    cv2.circle(image,(x,y),8,(155,20,255),-1)
    print("({}, {})".format(x,y))

cv2.imwrite('mask.png', mask)
cv2.imwrite('opening.png', opening)
cv2.imwrite('blank_mask.png', blank_mask)
cv2.imwrite('image.png', image)
cv2.imwrite('result.png', result)
cv2.waitKey()

