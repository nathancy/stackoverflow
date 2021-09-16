import cv2
import numpy as np

image = cv2.imread('1.png')
highlight = image.copy()
original = image.copy()

# Convert image to grayscale, Otsu's threshold, and find contours
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]

# Create black mask to extract desired objects
mask = np.zeros(image.shape, dtype=np.uint8)

# Search for objects by filtering using contour area and aspect ratio
for c in contours:
    # Contour area
    area = cv2.contourArea(c)
    # Contour perimeter
    peri = cv2.arcLength(c, True)
    # Contour approximation
    approx = cv2.approxPolyDP(c, 0.035 * peri, True)
    (x, y, w, h) = cv2.boundingRect(approx)
    aspect_ratio = w / float(h)
    # Draw filled contour onto mask if passes filter
    # These are arbitary values, may need to change depending on input image
    if aspect_ratio <= 1.2 or area < 5000:
        cv2.drawContours(highlight, [c], 0, (0,255,0), -1)
        cv2.drawContours(mask, [c], 0, (255,255,255), -1)

# Convert 3-channel mask to grayscale then bitwise-and with original image for result
mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
result = cv2.bitwise_and(original, original, mask=mask)

# Uncomment if you want background to be white instead of black
# result[mask==0] = (255,255,255)

# Display
cv2.imshow('gray', gray)
cv2.imshow('thresh', thresh)
cv2.imshow('highlight', highlight)
cv2.imshow('mask', mask)
cv2.imshow('result', result)

# Save images
# cv2.imwrite('gray.png', gray)
# cv2.imwrite('thresh.png', thresh)
# cv2.imwrite('highlight.png', highlight)
# cv2.imwrite('mask.png', mask)
# cv2.imwrite('result.png', result)
cv2.waitKey(0)
