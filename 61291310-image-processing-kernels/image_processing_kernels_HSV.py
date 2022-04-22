import cv2
import numpy as np

# Load image, convert to grayscale, Otsu's threshold, morph operations to remove noise
image = cv2.imread('1.jpg')
original = image.copy()
result_mask = np.zeros(image.shape, dtype=np.uint8)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
erode = cv2.erode(thresh, kernel, iterations=2)
morph = cv2.morphologyEx(erode, cv2.MORPH_CLOSE, kernel, iterations=3)

# Count number of kernels and average kernel area
number_of_kernels = 0
average_area = 0
cnts = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    # Filter out tiny specs of noise
    area = cv2.contourArea(c)
    if area > 10:
        number_of_kernels += 1
        average_area += area

average_area /= number_of_kernels
print('Number of kernels:', number_of_kernels)
print('Average kernel area: {:.3f}'.format(average_area))

# Perform HSV color thresholding
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower = np.array([0, 70, 97])
upper = np.array([179, 255, 255])
mask = cv2.inRange(hsv, lower, upper)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
cleanup = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=3)

# Find number of good kernels using an area threshold ratio relative to average kernel area
cnts = cv2.findContours(cleanup, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
area_threshold = 0.75
good_kernels = 0
for c in cnts:
    area = cv2.contourArea(c)
    if area > area_threshold * average_area:
        cv2.drawContours(image, [c], -1, (36,255,12), 4)
        cv2.drawContours(result_mask, [c], -1, (255,255,255), -1)
        good_kernels += 1

# Calculate number of infected kernels
result_mask = cv2.cvtColor(result_mask, cv2.COLOR_BGR2GRAY)
result = cv2.bitwise_and(original, original, mask=result_mask)
number_of_infected = number_of_kernels - good_kernels

print('Number of good kernels:', good_kernels)
print('Number of infected:', number_of_infected)
print('Percentage infected: {:.3f}%'.format((number_of_infected/number_of_kernels) * 100)) 

cv2.imshow('image', image)
cv2.imshow('thresh', thresh)
cv2.imshow('morph', morph)
cv2.imshow('result', result)
cv2.waitKey()
