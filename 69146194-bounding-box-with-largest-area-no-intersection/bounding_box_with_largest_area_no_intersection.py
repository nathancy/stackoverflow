import cv2
import numpy as np

# Check if C1 and C2 intersect
def contour_intersect(original_image, contour1, contour2):
    # Two separate contours trying to check intersection on
    contours = [contour1, contour2]

    # Create image filled with zeros the same size of original image
    blank = np.zeros(original_image.shape[0:2])

    # Copy each contour into its own image and fill it with '1'
    image1 = cv2.drawContours(blank.copy(), contours, 0, 1)
    image2 = cv2.drawContours(blank.copy(), contours, 1, 1)

    # Use the logical AND operation on the two images
    # Since the two images had bitwise and applied to it,
    # there should be a '1' or 'True' where there was intersection
    # and a '0' or 'False' where it didnt intersect
    intersection = np.logical_and(image1, image2)

    # Check if there was a '1' in the intersection
    return intersection.any()

# Check if C1 is in C2
def contour_inside(contour1, contour2):
    # Find centroid of C1
    M = cv2.moments(contour1)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])

    inside = cv2.pointPolygonTest(contour2, (cx, cy), False)

    if inside == 0 or inside == -1:
        return False
    elif inside == 1:
        return True

# Load image, convert to grayscale, Otsu's threshold
image = cv2.imread('1.png')
original = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Find contours, sort by contour area from largest to smallest
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
sorted_cnts = sorted(cnts, key=lambda x: cv2.contourArea(x), reverse=True)

# "Intersection" and "inside" contours
# Add both contours to test 
# --------------------------------
intersect_contour = np.array([[[230, 93]], [[230, 187]], [[326, 187]], [[326, 93]]])
sorted_cnts.append(intersect_contour)
cv2.drawContours(original, [intersect_contour], -1, (36,255,12), 3)

inside_contour = np.array([[[380, 32]], [[380, 229]], [[740, 229]], [[740, 32]]])
sorted_cnts.append(inside_contour)
cv2.drawContours(original, [inside_contour], -1, (36,255,12), 3)
# --------------------------------

# Find centroid for each contour and label contour number
for count, c in enumerate(sorted_cnts):
    M = cv2.moments(c)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    cv2.putText(original, str(count), (cx-5, cy+5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (246,255,12), 3)

# Find largest bounding box contour
largest_contour_name = ""
largest_contour = ""
contours_length = len(sorted_cnts)
for i1 in range(contours_length):
    found = True
    for i2 in range(i1 + 1, contours_length):
        c1 = sorted_cnts[i1]
        c2 = sorted_cnts[i2]
        
        # Test intersection and "inside" contour
        if contour_intersect(original, c1, c2) or contour_inside(c1, c2):
            print('Contour #{} has failed test'.format(i1))
            found = False
            continue
    if found:
        largest_contour_name = i1
        largest_contour = sorted_cnts[i1]
        break
print('Contour #{} is the largest'.format(largest_contour_name))
print(largest_contour)

# Display
cv2.imshow('thresh', thresh)
cv2.imshow('image', image)
cv2.imshow('original', original)
cv2.waitKey()
