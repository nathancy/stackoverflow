import cv2
import numpy as np

# Load image, grayscale, Otsu's threshold
image = cv2.imread('1.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Morph close
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=3)

# Create line mask and convex hull mask
line_mask = np.zeros(image.shape, dtype=np.uint8)
convex_mask = np.zeros(image.shape, dtype=np.uint8)

# Find convex hull on the binary image
cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnt = cnts[0]
hull = cv2.convexHull(cnt,returnPoints = False)
defects = cv2.convexityDefects(cnt,hull)
for i in range(defects.shape[0]):
    s,e,f,d = defects[i,0]
    start = tuple(cnt[s][0])
    end = tuple(cnt[e][0])
    far = tuple(cnt[f][0])
    cv2.line(convex_mask,start,end,[255,255,255],5)

# Morph close the convex hull mask, find contours, and fill in the outline
convex_mask = cv2.cvtColor(convex_mask, cv2.COLOR_BGR2GRAY)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
convex_mask = cv2.morphologyEx(convex_mask, cv2.MORPH_CLOSE, kernel, iterations=3)
cnts = cv2.findContours(convex_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cv2.fillPoly(convex_mask, cnts, (255,255,255))

# Perform linear regression on the binary image
[vx,vy,x,y] = cv2.fitLine(cnt,cv2.DIST_L2,0,0.01,0.01)
lefty = int((-x*vy/vx) + y)
righty = int(((image.shape[1]-x)*vy/vx)+y)
cv2.line(line_mask,(image.shape[1]-1,righty),(0,lefty),[255,255,255],2)

# Bitwise-and the line and convex hull masks together
result = cv2.bitwise_and(line_mask, line_mask, mask=convex_mask)
result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

# Find resulting contour and draw onto original image
cnts = cv2.findContours(result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cv2.drawContours(image, cnts, -1, (200,100,100), 3)

cv2.imshow('thresh', thresh)
cv2.imshow('close', close)
cv2.imshow('image', image)
cv2.imshow('line_mask', line_mask)
cv2.imshow('convex_mask', convex_mask)
cv2.imshow('result', result)
cv2.waitKey()

