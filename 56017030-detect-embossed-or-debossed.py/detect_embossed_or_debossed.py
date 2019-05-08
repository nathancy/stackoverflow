import numpy as np
import cv2

original_image = cv2.imread("1.jpg")
image = original_image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
morph = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
canny = cv2.Canny(morph, 130, 255, 1)

# Dilate canny image so contours connect and form a single contour
dilate = cv2.dilate(canny, kernel, iterations=4)

cv2.imshow("morph", morph)
cv2.imshow("canny", canny)
cv2.imshow("dilate", dilate)

# Find contours in the image
cnts = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

contours = []
# For each image separate it into top/bottom halfs
for c in cnts:
    # Obtain bounding rectangle for each contour
    x,y,w,h = cv2.boundingRect(c)

    # Draw bounding box rectangle
    cv2.rectangle(original_image,(x,y),(x+w,y+h),(0,255,0),3)
    # cv2.rectangle(original_image,(x,y),(x+w,y+h/2),(0,255,0),3) # top 
    # cv2.rectangle(original_image,(x,y+h/2),(x+w,y+h),(0,255,0),3) # bottom
    top_half = ((x,y), (x+w, y+h/2))
    bottom_half = ((x,y+h/2), (x+w, y+h))
    
    # Collect top/bottom ROIs
    contours.append((top_half, bottom_half))

for index, c in enumerate(contours):
    top_half, bottom_half = c

    top_x1,top_y1 = top_half[0]
    top_x2,top_y2 = top_half[1]
    bottom_x1,bottom_y1 = bottom_half[0]
    bottom_x2,bottom_y2 = bottom_half[1]
        
    # Grab ROI of top/bottom section from canny image
    top_image = canny[top_y1:top_y2, top_x1:top_x2]
    bottom_image = canny[bottom_y1:bottom_y2, bottom_x1:bottom_x2]
    
    cv2.imshow('top_image', top_image)
    cv2.imshow('bottom_image', bottom_image)

    # Count non-zero array elements
    top_pixels = cv2.countNonZero(top_image)
    bottom_pixels = cv2.countNonZero(bottom_image)

    print('top', top_pixels)
    print('bottom', bottom_pixels)

cv2.imshow("detected", original_image) 
print('contours detected: {}'.format(len(contours)))
cv2.waitKey(0)
