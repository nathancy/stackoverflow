import cv2
import numpy as np

# Load image, create blank mask, grayscale, Otsu's threshold
image = cv2.imread('1.jpg')
original = image.copy()
mask = np.zeros(image.shape, dtype=np.uint8)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Morph close
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=5)

# Find contours and filter using contour area + contour approximation
# Determine perfect circle contour then draw onto blank mask
cnts = cv2.findContours(close, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)
    area = cv2.contourArea(c)
    if len(approx) > 4 and area > 10000 and area < 500000:
        ((x, y), r) = cv2.minEnclosingCircle(c)
        cv2.circle(mask, (int(x), int(y)), int(r), (255, 255, 255), -1)
        cv2.circle(image, (int(x), int(y)), int(r), (36, 255, 12), 3)

# Extract ROI
mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
x,y,w,h = cv2.boundingRect(mask)
mask_ROI = mask[y:y+h, x:x+w]
image_ROI = original[y:y+h, x:x+w]

# Bitwise-and for result
result = cv2.bitwise_and(image_ROI, image_ROI, mask=mask_ROI)
result[mask_ROI==0] = (255,255,255) # Color background white

cv2.imwrite('close.png', close)
cv2.imwrite('thresh.png', thresh)
cv2.imwrite('image.png', image)
cv2.imwrite('mask.png', mask)
cv2.imwrite('result.png', result)
cv2.waitKey()

