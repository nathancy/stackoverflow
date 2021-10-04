import cv2
import numpy as np

# Load image, convert to grayscale, Otsu's threshold for binary image
image = cv2.imread('1.png')
mask = np.zeros(image.shape, dtype=np.uint8)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Find contours, find rotated rectangle, find contour area
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
contour_area = cv2.contourArea(cnts[0])
print('Contour area: {}'.format(contour_area))
rect = cv2.minAreaRect(cnts[0])
box = np.int0(cv2.boxPoints(rect))
cv2.drawContours(image, [box], 0, (36,255,12), 3)

# Find area of rotated bounding box and draw onto mask image
mask_area = cv2.contourArea(box)
cv2.drawContours(mask, [box], 0, (255,255,255), -1)
print('Mask area: {}'.format(mask_area))

# Compare areas and calculate percentage
rectangular_threshold = 80
percentage = (contour_area / mask_area) * 100
print('Compared area percentage: {:.3f}%'.format(percentage))
if percentage > rectangular_threshold:
    print('It is a rectangle!')
else:
    print('It is not a rectangle!')

# Display
cv2.imshow('image', image)
cv2.imshow('thresh', thresh)
cv2.imshow('mask', mask)
cv2.waitKey()
