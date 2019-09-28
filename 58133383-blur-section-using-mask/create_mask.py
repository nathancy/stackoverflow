import cv2
import numpy as np

# Create a mask
image = cv2.imread('1.png')
mask = np.zeros(image.shape, dtype=np.uint8)
cnt = np.array([[200, 100], [350, 100], [350, 250], [200, 250]])
cv2.fillPoly(mask, [cnt], [255,255,255])
cv2.imwrite('newmask.png', mask)
