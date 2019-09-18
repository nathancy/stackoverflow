import cv2
import numpy as np

# Grayscale, Otsu's threshold, opening
image = cv2.imread('1.png')
blank_mask = np.zeros(image.shape, dtype=np.uint8)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15,15))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)

inverse = 255 - opening
inverse = cv2.merge([inverse,inverse,inverse])
removed_artifacts = cv2.bitwise_and(image,image,mask=opening)
removed_artifacts = cv2.bitwise_or(removed_artifacts, inverse)

# Isolate blood vessels
veins_gray = cv2.cvtColor(removed_artifacts, cv2.COLOR_BGR2GRAY)
adaptive = cv2.adaptiveThreshold(veins_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,3)

cnts = cv2.findContours(adaptive, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

for c in cnts:
    area = cv2.contourArea(c)
    if area < 5000:
        cv2.drawContours(blank_mask, [c], -1, (255,255,255), 1)

blank_mask = cv2.cvtColor(blank_mask, cv2.COLOR_BGR2GRAY)
final = cv2.bitwise_and(image, image, mask=blank_mask)
# final[blank_mask==0] = (255,255,255) # White version

cv2.imshow('thresh', thresh)
cv2.imshow('opening', opening)
cv2.imshow('removed_artifacts', removed_artifacts)
cv2.imshow('adaptive', adaptive)
cv2.imshow('blank_mask', blank_mask)
cv2.imshow('final', final)
cv2.waitKey()
