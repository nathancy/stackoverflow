import numpy as np
import cv2

def rotate(image, angle):
    # Obtain the dimensions of the image
    (height, width) = image.shape[:2]
    (cX, cY) = (width / 2, height / 2)

    # Grab the rotation components of the matrix
    matrix = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(matrix[0, 0])
    sin = np.abs(matrix[0, 1])

    # Find the new bounding dimensions of the image
    new_width = int((height * sin) + (width * cos))
    new_height = int((height * cos) + (width * sin))

    # Adjust the rotation matrix to take into account translation
    matrix[0, 2] += (new_width / 2) - cX
    matrix[1, 2] += (new_height / 2) - cY

    # Perform the actual rotation and return the image
    return cv2.warpAffine(image, matrix, (new_width, new_height))

image = cv2.imread("1.PNG")
original_image = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3,3), 0)
thresh = cv2.threshold(blurred, 110, 255, cv2.THRESH_BINARY_INV)[1]
cv2.imshow("thresh", thresh)

x, y, w, h = 0, 0, image.shape[1], image.shape[0]

top_half = ((x,y), (x+w, y+h/2))
bottom_half = ((x,y+h/2), (x+w, y+h))

top_x1,top_y1 = top_half[0]
top_x2,top_y2 = top_half[1]
bottom_x1,bottom_y1 = bottom_half[0]
bottom_x2,bottom_y2 = bottom_half[1]

# Split into top/bottom ROIs
top_image = thresh[top_y1:top_y2, top_x1:top_x2]
bottom_image = thresh[bottom_y1:bottom_y2, bottom_x1:bottom_x2]

cv2.imshow("top_image", top_image)
cv2.imshow("bottom_image", bottom_image)

# Count non-zero array elements
top_pixels = cv2.countNonZero(top_image)
bottom_pixels = cv2.countNonZero(bottom_image)

print('top', top_pixels)
print('bottom', bottom_pixels)

# Rotate if upside down
if top_pixels > bottom_pixels:
    rotated = rotate(original_image, 180)
    cv2.imshow("rotated", rotated)

cv2.waitKey(0)
