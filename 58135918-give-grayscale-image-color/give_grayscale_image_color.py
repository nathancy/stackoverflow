import cv2
import numpy as np

before = cv2.imread('2.png')
b, g, r = cv2.split(before)

np.multiply(b, 1.5, out=b, casting="unsafe")
np.multiply(g, .75, out=g, casting="unsafe")
np.multiply(r, 1.25, out=r, casting="unsafe")

after = cv2.merge([b, g, r])

cv2.imshow('before', before)
cv2.imshow('after', after)
cv2.waitKey()
