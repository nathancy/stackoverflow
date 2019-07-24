import cv2
import numpy as np

def rotate_image(image, angle):
    # Grab the dimensions of the image and then determine the center
    (h, w) = image.shape[:2]
    (cX, cY) = (w / 2, h / 2)
    
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # Compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # Adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # Perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))

def order_points_clockwise(pts):
    # sort the points based on their x-coordinates
    xSorted = pts[np.argsort(pts[:, 0]), :]

    # grab the left-most and right-most points from the sorted
    # x-roodinate points
    leftMost = xSorted[:2, :]
    rightMost = xSorted[2:, :]

    # now, sort the left-most coordinates according to their
    # y-coordinates so we can grab the top-left and bottom-left
    # points, respectively
    leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
    (tl, bl) = leftMost

    # now, sort the right-most coordinates according to their
    # y-coordinates so we can grab the top-right and bottom-right
    # points, respectively
    rightMost = rightMost[np.argsort(rightMost[:, 1]), :]
    (tr, br) = rightMost

    # return the coordinates in top-left, top-right,
    # bottom-right, and bottom-left order
    return np.array([tl, tr, br, bl], dtype="int32")

def perspective_transform(image, corners):
    def order_corner_points(corners):
        # Separate corners into individual points
        # Index 0 - top-right
        #       1 - top-left
        #       2 - bottom-left
        #       3 - bottom-right
        corners = [(corner[0][0], corner[0][1]) for corner in corners]
        top_r, top_l, bottom_l, bottom_r = corners[0], corners[1], corners[2], corners[3]
        return (top_l, top_r, bottom_r, bottom_l)

    # Order points in clockwise order
    ordered_corners = order_corner_points(corners)
    top_l, top_r, bottom_r, bottom_l = ordered_corners
    
    # Determine width of new image which is the max distance between 
    # (bottom right and bottom left) or (top right and top left) x-coordinates
    width_A = np.sqrt(((bottom_r[0] - bottom_l[0]) ** 2) + ((bottom_r[1] - bottom_l[1]) ** 2))
    width_B = np.sqrt(((top_r[0] - top_l[0]) ** 2) + ((top_r[1] - top_l[1]) ** 2))
    width = max(int(width_A), int(width_B))

    # Determine height of new image which is the max distance between 
    # (top right and bottom right) or (top left and bottom left) y-coordinates
    height_A = np.sqrt(((top_r[0] - bottom_r[0]) ** 2) + ((top_r[1] - bottom_r[1]) ** 2))
    height_B = np.sqrt(((top_l[0] - bottom_l[0]) ** 2) + ((top_l[1] - bottom_l[1]) ** 2))
    height = max(int(height_A), int(height_B))

    # Construct new points to obtain top-down view of image in 
    # top_r, top_l, bottom_l, bottom_r order
    dimensions = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], 
                    [0, height - 1]], dtype = "float32")
    
    # Convert to Numpy format
    ordered_corners = np.array(ordered_corners, dtype="float32")

    # Find perspective transform matrix
    matrix = cv2.getPerspectiveTransform(ordered_corners, dimensions)

    # Return the transformed image
    return cv2.warpPerspective(image, matrix, (width, height))

image = cv2.imread('1.jpg')
original = image.copy()

mask = np.zeros(image.shape, np.uint8)
clean_mask = np.zeros(image.shape, np.uint8)
blur = cv2.medianBlur(image, 9)
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray, 120, 255, 1)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
close = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel, iterations=2)
dilate = cv2.dilate(close, kernel, iterations=1)

minLineLength = 150
maxLineGap = 250
lines = cv2.HoughLinesP(dilate,1,np.pi/180,100,minLineLength,maxLineGap)
for line in lines:
    for x1,y1,x2,y2 in line:
        cv2.line(mask,(x1,y1),(x2,y2),(255,255,255),2)

mask = cv2.dilate(mask, kernel, iterations=2)
mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
cv2.imwrite('mask.png', mask)

corners = cv2.goodFeaturesToTrack(mask,4,0.5,1000)

c_list = []
for corner in corners:
    x,y = corner.ravel()
    c_list.append([int(x), int(y)])
    cv2.circle(image,(x,y),40,(36,255,12),-1)

cv2.imwrite('corner_points.png', image)
corner_points = np.array([c_list[0], c_list[1], c_list[2], c_list[3]])
ordered_corner_points = order_points_clockwise(corner_points)
ordered_corner_points = np.array(ordered_corner_points).reshape((-1,1,2)).astype(np.int32)

cv2.drawContours(clean_mask, [ordered_corner_points], -1, (255, 255, 255), 2)

cv2.imwrite('clean_mask.png', clean_mask)
clean_mask = cv2.cvtColor(clean_mask, cv2.COLOR_BGR2GRAY)
cnts = cv2.findContours(clean_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

for c in cnts:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.015 * peri, True)

    if len(approx) == 4:
        transformed = perspective_transform(original, approx)

# Rotate image
result = rotate_image(transformed, -90)

cv2.imshow('image', image)
cv2.imwrite('close.png', close)
cv2.imwrite('canny.png', canny)
cv2.imwrite('dilate.png', dilate)
cv2.imshow('clean_mask', clean_mask)
cv2.imwrite('image.png', image)
cv2.imshow('result', result)
cv2.imwrite('result.png', result)
cv2.waitKey()

