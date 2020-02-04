import numpy as np
import cv2
import imutils

# Load images
image1 = cv2.imread('1.jpg', 0)
image2 = cv2.imread('2.jpg', 0)

# Enlarge images
image1 = imutils.resize(image1, width=400)
image2 = imutils.resize(image2, width=400)

# Create the sift object
sift = cv2.xfeatures2d.SIFT_create(700)

# Find keypoints and descriptors directly
kp1, des1 = sift.detectAndCompute(image2, None)
kp2, des2 = sift.detectAndCompute(image1, None)

# FLANN parameters
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)   # or pass empty dictionary
flann = cv2.FlannBasedMatcher(index_params,search_params)
matches = flann.knnMatch(des1,des2,k=2)

# Need to draw only good matches, so create a mask
matchesMask = [[0,0] for i in range(len(matches))]

count = 0
# Ratio test as per Lowe's paper (0.7)
# Modify to change threshold 
for i,(m,n) in enumerate(matches):
    if m.distance < 0.4*n.distance:
        count += 1
        matchesMask[i]=[1,0]

# Draw lines
draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   matchesMask = matchesMask,
                   flags = 0)

# Display the matches
result = cv2.drawMatchesKnn(image2,kp1,image1,kp2,matches,None,**draw_params)
print('Matches:', count)
cv2.imshow('result', result)
cv2.waitKey()
