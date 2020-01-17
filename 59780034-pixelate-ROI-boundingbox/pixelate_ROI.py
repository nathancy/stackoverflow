import cv2

def pixelate(image):
    # Get input size
    width, height, _ = image.shape

    # Desired "pixelated" size
    w, h = (16, 16)

    # Resize image to "pixelated" size
    temp = cv2.resize(image, (h, w), interpolation=cv2.INTER_LINEAR)

    # Initialize output image
    return cv2.resize(temp, (height, width), interpolation=cv2.INTER_NEAREST)

# Load image
image = cv2.imread('1.png')

# ROI bounding box coordinates
x,y,w,h = 122,98,283,240

# Extract ROI
ROI = image[y:y+h, x:x+w]

# Pixelate ROI
pixelated_ROI = pixelate(ROI)

# Paste pixelated ROI back into original image
image[y:y+h, x:x+w] = pixelated_ROI

cv2.imshow('pixelated_ROI', pixelated_ROI)
cv2.imshow('image', image)
cv2.waitKey()
