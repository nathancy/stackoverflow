import cv2
import numpy as np

# Load image, convert to grayscale, threshold
image = cv2.imread('1.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Find convex hull and draw onto a mask
mask = np.zeros(image.shape, dtype=np.uint8)
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnt = cnts[0]
hull = cv2.convexHull(cnt,returnPoints = False)
defects = cv2.convexityDefects(cnt,hull)
for i in range(defects.shape[0]):
    s,e,f,d = defects[i,0]
    start = tuple(cnt[s][0])
    end = tuple(cnt[e][0])
    far = tuple(cnt[f][0])
    cv2.line(mask,start,end,[255,255,255],3)

# Morph close to fill small holes
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
close = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

# Draw outline around input image
close = cv2.cvtColor(close, cv2.COLOR_BGR2GRAY)
cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cv2.drawContours(image,cnts,0,(36,255,12),1)

cv2.imshow('image', image)
cv2.waitKey()
