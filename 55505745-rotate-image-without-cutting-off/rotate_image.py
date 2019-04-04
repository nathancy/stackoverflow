import cv2
import numpy as np

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

img = cv2.imread('placeholder4.PNG')
rotated = rotate(img, -90)

cv2.imshow('original', img)
cv2.imshow('rotated', rotated)
cv2.waitKey(0)
