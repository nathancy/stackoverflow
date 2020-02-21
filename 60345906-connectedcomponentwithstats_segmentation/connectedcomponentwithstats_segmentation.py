import cv2
import numpy as np

# Load image, Gaussian blur, grayscale, Otsu's threshold
image = cv2.imread('2.jpg')
blur = cv2.GaussianBlur(image, (3,3), 0)
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Perform connected component labeling
n_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh, connectivity=4)

# Create false color image and color background black
colors = np.random.randint(0, 255, size=(n_labels, 3), dtype=np.uint8)
colors[0] = [0, 0, 0]  # for cosmetic reason we want the background black
false_colors = colors[labels]

# Label area of each polygon
false_colors_area = false_colors.copy()
for i, centroid in enumerate(centroids[1:], start=1):
    area = stats[i, 4]
    cv2.putText(false_colors_area, str(area), (int(centroid[0]), int(centroid[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

cv2.imshow('thresh', thresh)
cv2.imshow('false_colors', false_colors)
cv2.imshow('false_colors_area', false_colors_area)
cv2.waitKey()
