from matplotlib import pyplot as plt
import cv2

image = cv2.imread('1.png')

channels = cv2.split(image)
colors = ("b", "g", "r")

plt.figure()
plt.title("Color Histogram")
plt.xlabel("Bins")
plt.ylabel("# of Pixels")
features = []
 
# Loop over the image channels (B, G, R)
for (channel, color) in zip(channels, colors):
    
    # Calculate histogram
    hist = cv2.calcHist([channel], [0], None, [255], [1, 256])
    features.extend(hist)
    
    # Plot histogram
    plt.plot(hist, color = color)
    plt.xlim([0, 256])

plt.show()
