
import cv2
# Resizes a image and maintains aspect ratio
def maintain_aspect_ratio_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # Grab the image size and initialize dimensions
    dim = None
    (h, w) = image.shape[:2]

    # Return original image if no need to resize
    if width is None and height is None:
        return image

    # We are resizing height if width is none
    if width is None:
        # Calculate the ratio of the height and construct the dimensions
        r = height / float(h)
        dim = (int(w * r), height)
    # We are resizing width if height is none
    else:
        # Calculate the ratio of the 0idth and construct the dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # Return the resized image
    return cv2.resize(image, dim, interpolation=inter)


image = cv2.imread('1.png')
cv2.imshow('width_100', maintain_aspect_ratio_resize(image, width=100))
cv2.imshow('width_300', maintain_aspect_ratio_resize(image, width=300))

cv2.imwrite('2.png', maintain_aspect_ratio_resize(image, width=100))
cv2.imwrite('3.png', maintain_aspect_ratio_resize(image, width=300))

cv2.waitKey()
