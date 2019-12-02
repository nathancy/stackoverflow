import cv2
import numpy as np

# Load image, grayscale, and Otsu's threshold
image = cv2.imread('1.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Compute rotated bounding box
coords = np.column_stack(np.where(thresh > 0))
angle = cv2.minAreaRect(coords)[-1]

# Determine rotation angle
if angle < -45:
    angle = -(90 + angle)
else:
    angle = -angle
print(angle)

# Rotate image to deskew
(h, w) = image.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

# Vertical image so rotate to horizontal
h, w, _ = rotated.shape
if h > w:
    rotated = cv2.rotate(rotated, cv2.ROTATE_90_CLOCKWISE)

cv2.imshow('rotated', rotated)
cv2.imwrite('rotated.png', rotated)
cv2.waitKey()

