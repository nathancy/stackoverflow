import cv2

# Read in image
image = cv2.imread('1.png')

# Create ROI coordinates
topLeft = (60, 40)
bottomRight = (340, 120)
x, y = topLeft[0], topLeft[1]
w, h = bottomRight[0] - topLeft[0], bottomRight[1] - topLeft[1]

# Grab ROI with Numpy slicing and blur
ROI = image[y:y+h, x:x+w]
blur = cv2.GaussianBlur(ROI, (51,51), 0) 

# Insert ROI back into image
image[y:y+h, x:x+w] = blur

cv2.imshow('blur', blur)
cv2.imshow('image', image)
cv2.waitKey()
