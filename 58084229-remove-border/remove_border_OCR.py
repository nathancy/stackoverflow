import cv2

image = cv2.imread('1.png')
removed = image.copy()
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Remove horizontal lines
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,1))
remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
cnts = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    cv2.drawContours(removed, [c], -1, (255,255,255), 5)

# Remove vertical lines
vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,40))
remove_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
cnts = cv2.findContours(remove_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    cv2.drawContours(removed, [c], -1, (255,255,255), 15)

# Repair kernel
repair_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
removed = 255 - removed
dilate = cv2.dilate(removed, repair_kernel, iterations=5)
dilate = cv2.cvtColor(dilate, cv2.COLOR_BGR2GRAY)
pre_result = cv2.bitwise_and(dilate, thresh)

result = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, repair_kernel, iterations=5)
final = cv2.bitwise_and(result, thresh)

invert_final = 255 - final

cv2.imshow('thresh', thresh)
cv2.imshow('removed', removed)
cv2.imshow('dilate', dilate)
cv2.imshow('pre_result', pre_result)
cv2.imshow('result', result)
cv2.imshow('final', final)
cv2.imshow('invert_final', invert_final)
cv2.waitKey()
