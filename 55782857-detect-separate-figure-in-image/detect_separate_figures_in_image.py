import numpy as np
import cv2

original_image = cv2.imread("1.png")
image = original_image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
canny = cv2.Canny(blurred, 120, 255, 1)

cv2.imshow("blurred", blurred)
cv2.imshow("canny", canny)

# Find contours in the image
cnts = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

contours = []

for c in cnts:
    # Obtain bounding rectangle for each contour
    x,y,w,h = cv2.boundingRect(c)

    # Find ROI of the contour
    roi = image[y:y+h, x:x+w]
    
    # Draw bounding box rectangle
    cv2.rectangle(original_image,(x,y),(x+w,y+h),(0,255,0),3)
    contours.append(c)

cv2.imshow("detected", original_image) 
print('contours detected: {}'.format(len(contours)))
cv2.waitKey(0)
