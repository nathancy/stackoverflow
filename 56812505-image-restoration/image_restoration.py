from matplotlib import pyplot as plt
import cv2

# Load in image as grayscale
image = cv2.imread('1.jpg', 0)

clahe = cv2.createCLAHE().apply(image)
equalize = cv2.equalizeHist(image)

plt.subplot(1,3,1)
plt.hist(image.ravel(), 256, [0,256])
plt.title('Original')
plt.xlabel('Pixel Values')
plt.ylabel('No. of Pixels')

plt.subplot(1,3,2)
plt.hist(equalize.ravel(), 256, [0,256])
plt.title('Equalize')
plt.xlabel('Pixel Values')
plt.ylabel('No. of Pixels')

plt.subplot(1,3,3)
plt.hist(clahe.ravel(), 256, [0,256])
plt.title('CLAHE')
plt.xlabel('Pixel Values')
plt.ylabel('No. of Pixels')

plt.tight_layout()
plt.show()

cv2.imshow('image', image)
cv2.imshow('clahe',clahe)
cv2.imshow('equalize',equalize)
cv2.waitKey(0)
