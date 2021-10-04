import cv2

# Load image and create a "overlay" image (copy of input image)
image = cv2.imread('2.jpg')
overlay = image.copy()
original = image.copy() # To show no transparency

# Test coordinates to draw a line
x, y, w, h = 108, 107, 193, 204

# Draw line on overlay and original input image to show difference
cv2.line(overlay, (x, y), (x + w, x + h), (36, 255, 12), 6)
cv2.line(original, (x, y), (x + w, x + h), (36, 255, 12), 6)

# Could also work with any other drawing function
# cv2.rectangle(overlay, (x, y), (x + w, y + h), (36, 255, 12), -1)
# cv2.rectangle(original, (x, y), (x + w, y + h), (36, 255, 12), -1)
# cv2.circle(overlay, (x, y), 80, (36, 255, 12), -1)
# cv2.circle(original, (x, y), 80, (36, 255, 12), -1)

# Transparency value
alpha = 0.50

# Perform weighted addition of the input image and the overlay
result = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

cv2.imshow('result', result)
cv2.imshow('original', original)
cv2.waitKey()
