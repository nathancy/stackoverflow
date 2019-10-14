import numpy as np
import cv2

image = cv2.imread('1.jpg')
sharpen = np.array([[0, -1, 0], 
                    [-1, 5, -1], 
                    [0, -1, 0]])
print(sharpen)
sharpen_result = cv2.filter2D(image, -1, sharpen)
cv2.imshow('sharpen_result', sharpen_result)
cv2.imwrite('sharpen_result.png', sharpen_result)

laplacian = np.array([[0, 1, 0], 
                      [1, -4, 1], 
                      [0, 1, 0]])

print(laplacian)
laplacian_result = cv2.filter2D(image, -1, laplacian)
cv2.imshow('laplacian_result', laplacian_result)
cv2.imwrite('laplacian_result.png', laplacian_result)

emboss = np.array([[-2, -1, 0], 
                   [-1, 1, 1], 
                   [0, 1, 2]])

print(emboss)
emboss_result = cv2.filter2D(image, -1, emboss)
cv2.imshow('emboss_result', emboss_result)
cv2.imwrite('emboss_result.png', emboss_result)

outline = np.array([[-1, -1, -1], 
                    [-1, 8, -1], 
                    [-1, -1, -1]])

print(outline)
outline_result = cv2.filter2D(image, -1, outline)
cv2.imshow('outline_result', outline_result)
cv2.imwrite('outline_result.png', outline_result)

bottom_sobel = np.array([[-1, -2, -1], 
                         [0, 0, 0], 
                         [1, 2, 1]])

print(bottom_sobel)
bottom_sobel_result = cv2.filter2D(image, -1, bottom_sobel)
cv2.imshow('bottom_sobel_result', bottom_sobel_result)
cv2.imwrite('bottom_sobel_result.png', bottom_sobel_result)

left_sobel = np.array([[1, 0, -1], 
                       [2, 0, -2], 
                       [1, 0, -1]])

print(left_sobel)
left_sobel_result = cv2.filter2D(image, -1, left_sobel)
cv2.imshow('left_sobel_result', left_sobel_result)
cv2.imwrite('left_sobel_result.png', left_sobel_result)

right_sobel = np.array([[-1, 0, 1], 
                        [-2, 0, 2], 
                        [-1, 0, 1]])

print(right_sobel)
right_sobel_result = cv2.filter2D(image, -1, right_sobel)
cv2.imshow('right_sobel_result', right_sobel_result)
cv2.imwrite('right_sobel_result.png', right_sobel_result)

top_sobel = np.array([[1, 2, 1], 
                      [0, 0, 0], 
                      [-1, -2, -1]])

print(top_sobel)
top_sobel_result = cv2.filter2D(image, -1, top_sobel)
cv2.imshow('top_sobel_result', top_sobel_result)
cv2.imwrite('top_sobel_result.png', top_sobel_result)

cv2.waitKey()
