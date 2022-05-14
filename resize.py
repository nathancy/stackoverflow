import cv2
import imutils

image = cv2.imread('./test/1.png')
image = imutils.resize(image, width=600)
cv2.imwrite('1.png', image)
