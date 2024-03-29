import cv2
import numpy as np
from sklearn.cluster import KMeans

def visualize_colors(cluster, centroids, exact=False):
    # Get the number of different clusters, create histogram, and normalize
    labels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
    (hist, _) = np.histogram(cluster.labels_, bins = labels)
    hist = hist.astype("float")
    hist /= hist.sum()
    
    # Convert each RGB color code from float to int
    if not exact:
        centroids = centroids.astype("int")
    
    # Create frequency rect and iterate through each cluster's color and percentage
    rect = np.zeros((50, 300, 3), dtype=np.uint8)
    colors = sorted([(percent, color) for (percent, color) in zip(hist, centroids)])
    start = 0
    for (percent, color) in colors:
        print(color, "{:0.2f}%".format(percent * 100))
        end = start + (percent * 300)
        cv2.rectangle(rect, (int(start), 0), (int(end), 50), \
                      color.astype("uint8").tolist(), -1)
        start = end
    return colors, rect

# Load image and convert to a list of pixels
image = cv2.imread('4.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
reshape = image.reshape((image.shape[0] * image.shape[1], 3))

# Find and display most X dominant colors
cluster = KMeans(n_clusters=5).fit(reshape)
colors, visualize = visualize_colors(cluster, cluster.cluster_centers_)
visualize = cv2.cvtColor(visualize, cv2.COLOR_RGB2BGR)

# Obtain dominant RGB color code
dominant_color = colors[-1][1].tolist()
dominant_color_average = sum(dominant_color)
print('Dominant color:', dominant_color)
print('Dominant color average:', int(dominant_color_average / 3))

# Find best color
if dominant_color_average <= 85:
    print('White!')
elif dominant_color_average > 85 and dominant_color_average <= 170:
    print('Gray!')
elif dominant_color_average > 170:
    print('Black!')

cv2.imshow('visualize', visualize)
cv2.waitKey()
