import cv2

image = cv2.imread('4.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
blur = cv2.medianBlur(gray, 25)
thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,27,6)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
dilate = cv2.dilate(close, kernel, iterations=2)

cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]

minimum_area = 500
for c in cnts:
    area = cv2.contourArea(c)
    if area > minimum_area:
        # Find centroid
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(image, (cX, cY), 20, (36, 255, 12), 2) 
        x,y,w,h = cv2.boundingRect(c)
        cv2.putText(image, 'Radius: {}'.format(w/2), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36,255,12), 2)
        break

cv2.imshow('thresh', thresh)
cv2.imshow('close', close)
cv2.imshow('image', image)
cv2.waitKey()
