from skimage.measure import compare_ssim
import cv2

image1 = cv2.imread('1.png')
image2 = cv2.imread('2.png')

# Convert images to grayscale
image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

# Compute SSIM between two images
(score, diff) = compare_ssim(image1_gray, image2_gray, full=True)
print("Image similarity:", score)

# The diff image contains the actual image differences between the two images
# and is represented as a floating point data type in the range [0,1] 
# so we must convert the array to 8-bit unsigned integers in the range
# [0,255] image1 we can use it with OpenCV
diff = (diff * 255).astype("uint8")

cv2.imshow('diff', diff)
cv2.waitKey()
