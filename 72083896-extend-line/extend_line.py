import numpy as np
import cv2
import math

"""
@param: dimensions - image shape from Numpy (h, w, c)
@param: p1 - starting point (x1, y1)
@param: p2 - ending point (x2, y2)
@param: SCALE - default parameter to ensure that extended lines go through borders
"""
def extend_line(dimensions, p1, p2, SCALE=10):
    # Calculate the intersection point given (x1, y1) and (x2, y2)
    def line_intersection(line1, line2):
        x_diff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        y_diff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def detect(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = detect(x_diff, y_diff)
        if div == 0:
           raise Exception('lines do not intersect')

        dist = (detect(*line1), detect(*line2))
        x = detect(dist, x_diff) / div
        y = detect(dist, y_diff) / div
        return int(x), int(y)

    x1, x2 = 0, 0
    y1, y2 = 0, 0
    
    # Extract w and h regardless of grayscale or BGR image
    if len(dimensions) == 3:
        h, w, _ = dimensions
    elif len(dimensions) == 2:
        h, w = dimensions
    
    # Take longest dimension and use it as maxed out distance
    if w > h:
        distance = SCALE * w
    else:
        distance = SCALE * h
    
    # Reorder smaller X or Y to be the first point
    # and larger X or Y to be the second point
    try:
        slope = (p2[1] - p1[1]) / (p1[0] - p2[0])
        # HORIZONTAL or DIAGONAL
        if p1[0] <= p2[0]:
            x1, y1 = p1
            x2, y2 = p2
        else:
            x1, y1 = p2
            x2, y2 = p1
    except ZeroDivisionError:
        # VERTICAL
        if p1[1] <= p2[1]:
            x1, y1 = p1
            x2, y2 = p2
        else:
            x1, y1 = p2
            x2, y2 = p1
    
    # Extend after end-point A
    length_A = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    p3_x = int(x1 + (x1 - x2) / length_A * distance)
    p3_y = int(y1 + (y1 - y2) / length_A * distance)

    # Extend after end-point B
    length_B = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    p4_x = int(x2 + (x2 - x1) / length_B * distance)
    p4_y = int(y2 + (y2 - y1) / length_B * distance)
   
    # -------------------------------------- 
    # Limit coordinates to borders of image
    # -------------------------------------- 
    # HORIZONTAL
    if y1 == y2:
        if p3_x < 0: 
            p3_x = 0
        if p4_x > w: 
            p4_x = w
        return ((p3_x, p3_y), (p4_x, p4_y))
    # VERTICAL
    elif x1 == x2:
        if p3_y < 0: 
            p3_y = 0
        if p4_y > h: 
            p4_y = h
        return ((p3_x, p3_y), (p4_x, p4_y))
    # DIAGONAL
    else:
        A = (p3_x, p3_y)
        B = (p4_x, p4_y)

        C = (0, 0)  # C-------D
        D = (w, 0)  # |-------|
        E = (w, h)  # |-------|
        F = (0, h)  # F-------E
        
        if slope > 0:
            # 1st point, try C-F side first, if OTB then F-E
            new_x1, new_y1 = line_intersection((A, B), (C, F))
            if new_x1 > w or new_y1 > h:
                new_x1, new_y1 = line_intersection((A, B), (F, E))

            # 2nd point, try C-D side first, if OTB then D-E
            new_x2, new_y2 = line_intersection((A, B), (C, D))
            if new_x2 > w or new_y2 > h:
                new_x2, new_y2 = line_intersection((A, B), (D, E))

            return ((new_x1, new_y1), (new_x2, new_y2))
        elif slope < 0:
            # 1st point, try C-F side first, if OTB then C-D
            new_x1, new_y1 = line_intersection((A, B), (C, F))
            if new_x1 < 0 or new_y1 < 0:
                new_x1, new_y1 = line_intersection((A, B), (C, D))
            # 2nd point, try F-E side first, if OTB then E-D
            new_x2, new_y2 = line_intersection((A, B), (F, E))
            if new_x2 > w or new_y2 > h:
                new_x2, new_y2 = line_intersection((A, B), (E, D))
            return ((new_x1, new_y1), (new_x2, new_y2))

# Vertical
# -------------------------------
# p1 = (250, 100)
# p2 = (250, 300)
# -------------------------------

# Horizontal
# -------------------------------
# p1 = (100, 300)
# p2 = (400, 300)
# -------------------------------

# Positive slope
# -------------------------------
# C-F, C-D
# p1 = (50, 400)
# p2 = (400, 50)

# C-F, E-D
# p1 = (50, 400)
# p2 = (400, 50)

# F-E, E-D
# p2 = (250, 400)
# p1 = (400, 250)

# F-E, C-D
# p2 = (250, 400)
# p1 = (300, 250)
# -------------------------------

# Negative slope
# -------------------------------
# C-F, E-D
# p1 = (100, 200)
# p2 = (450, 400)

# C-F, F-E
# p2 = (100, 200)
# p1 = (250, 400)

# C-D, D-E
# p1 = (100, 50)
# p2 = (450, 400)

# C-D, F-E
p1 = (100, 50)
p2 = (250, 400)
# -------------------------------

# Exact corner diagonals
# -------------------------------
# p1 = (50,50)
# p2 = (300, 300)

# p2 = (375, 125)
# p1 = (125, 375)
# -------------------------------

image = np.zeros((500,500,3), dtype=np.uint8)
p3, p4 = extend_line(image.shape, p1, p2)
print(p3, p4)
cv2.line(image, p3, p4, [255,255,255], 2)
cv2.line(image, p1, p3, [36,255,12], 2)
cv2.line(image, p2, p4, [36,255,12], 2)
cv2.imshow('image', image)
cv2.waitKey()
