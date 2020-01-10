import cv2
import numpy as np 
import matplotlib.pyplot as plt

# Load image, grayscale, Otsu's threshold
image = cv2.imread('1.png')
h, w = image.shape[:2]
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Sum white pixels in each row
# Create blank space array and and final image 
pixels = np.sum(thresh, axis=1).tolist()
space = np.ones((1, w), dtype=np.uint8) * 255
result = np.zeros((0, w), dtype=np.uint8)

# Iterate through each row and add space if entire row is empty
# otherwise add original section of image to final image
for index, value in enumerate(pixels):
    if value == 0:
        result = np.concatenate((result, space), axis=0)
    row = gray[index:index+1, 0:w]
    result = np.concatenate((result, row), axis=0)

plt.plot(pixels)
cv2.imshow('result', result)
cv2.imshow('thresh', thresh)
plt.show()
