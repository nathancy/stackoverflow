import cv2
import numpy as np

def contourIntersect(original_image, contour1, contour2):
    # Two separate contours trying to check intersection on
    contours = [contour1, contour2]

    # Create image filled with zeros the same size of original image
    blank = np.zeros(original_image.shape[0:2])

    # Copy each contour into its own image and fill it with '1'
    image1 = cv2.drawContours(blank.copy(), contours, 0, 1)
    image2 = cv2.drawContours(blank.copy(), contours, 1, 1)
    
    # Use the logical AND operation on the two images
    # Since the two images had bitwise AND applied to it,
    # there should be a '1' or 'True' where there was intersection
    # and a '0' or 'False' where it didnt intersect
    intersection = np.logical_and(image1, image2)
    
    # Check if there was a '1' in the intersection array
    return True if True in intersection else False

original_image = cv2.imread("base.png")
image = original_image.copy()

cv2.imshow("original", image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("gray", gray)
blurred = cv2.GaussianBlur(gray, (5,5), 0)
cv2.imshow("blur", blurred)
threshold = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
cv2.imshow("thresh", threshold)

contours = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# Depending on OpenCV version, number of arguments return by cv.findContours 
# is either 2 or 3
contours = contours[1] if len(contours) == 3 else contours[0]

contour_list = []
for c in contours:
    contour_list.append(c)
    cv2.drawContours(image, [c], 0, (0,255,0), 2)

print(contourIntersect(original_image, contour_list[0], contour_list[1]))
cv2.imshow("contour", image)
cv2.waitKey(0)
