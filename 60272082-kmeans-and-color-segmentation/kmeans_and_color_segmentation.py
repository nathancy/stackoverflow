import cv2
import numpy as np

# Kmeans color segmentation
def kmeans_color_quantization(image, clusters=8, rounds=1):
    h, w = image.shape[:2]
    samples = np.zeros([h*w,3], dtype=np.float32)
    count = 0

    for x in range(h):
        for y in range(w):
            samples[count] = image[x][y]
            count += 1

    compactness, labels, centers = cv2.kmeans(samples,
            clusters, 
            None,
            (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001), 
            rounds, 
            cv2.KMEANS_RANDOM_CENTERS)

    centers = np.uint8(centers)
    res = centers[labels.flatten()]
    return res.reshape((image.shape))

# Load original image
original = cv2.imread('2.png')

# Perform kmeans color segmentation
kmeans = kmeans_color_quantization(original, clusters=5)

# Color threshold on kmeans image
hsv = cv2.cvtColor(kmeans, cv2.COLOR_BGR2HSV)
lower = np.array([90, 0, 0])
upper = np.array([102, 255, 255])
mask = cv2.inRange(hsv, lower, upper)

# Apply mask onto original image
result = cv2.bitwise_and(original, original, mask=mask)
result[mask==0] = (255,255,255)

# Display
cv2.imshow('kmeans', kmeans)
cv2.imshow('result', result)
cv2.imshow('mask', mask)
cv2.waitKey()
