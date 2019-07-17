import cv2

image = cv2.imread('2.png')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray,120, 255,cv2.THRESH_BINARY_INV)[1]
cnts, h = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

label = '1'
count = 0

# Get inner list of hierarchy
for layer in zip(cnts, h[0]):
    contour = layer[0]
    hierarchy = layer[1]
    
    # If we find new contour (not inner) reset label
    if hierarchy[1] >= 0:
        label = '1'
    # Ensure that we only have outer contour
    if count % 2 == 0:
        cv2.drawContours(image, [contour], -1, (36, 255, 12), 2)
        x,y,w,h = cv2.boundingRect(contour)
        cv2.putText(image, label, (x +50,y+ 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (36,255,12), 3)
        label = str(int(label) * -1)
    
    count += 1
    
cv2.imshow('thresh', thresh)
cv2.imshow('image', image)
cv2.waitKey()

