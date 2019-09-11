import cv2
import numpy as np

def rotational_shift(image1, image2):
    def compute_angle(image):
        # Convert to grayscale, invert, and Otsu's threshold
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = 255 - gray
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Find coordinates of all pixel values greater than zero
        # then compute minimum rotated bounding box of all coordinates
        coords = np.column_stack(np.where(thresh > 0))
        angle = cv2.minAreaRect(coords)[-1]
        
        # The cv2.minAreaRect() function returns values in the range
        # [-90, 0) so need to correct angle
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        
        # Rotate image to horizontal position 
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, \
                  borderMode=cv2.BORDER_REPLICATE)

        return (angle, rotated)

    angle1, rotated1 = compute_angle(image1)
    angle2, rotated2 = compute_angle(image2)
    
    # Both angles are positive
    if angle1 >= 0 and angle2 >= 0:
        difference_angle = abs(angle1 - angle2)
    # One positive, one negative
    elif (angle1 < 0 and angle2 > 0) or (angle1 > 0 and angle2 < 0):
        difference_angle = abs(angle1) + abs(angle2)
    # Both negative
    elif angle1 < 0 and angle2 < 0:
        angle1 = abs(angle1)
        angle2 = abs(angle2)
        difference_angle = max(angle1, angle2) - min(angle1, angle2)

    return (difference_angle, rotated1, rotated2)

if __name__ == '__main__':
    image1 = cv2.imread('pos_7_9.png')
    image2 = cv2.imread('neg_35.png')

    angle, rotated1, rotated2 = rotational_shift(image1, image2)
    print(angle)
