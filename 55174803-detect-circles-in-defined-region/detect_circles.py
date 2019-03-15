import cv2
import numpy as np

class DetectCirclesWidget(object):
    def __init__(self):
        self.original_image = cv2.imread('circles.PNG')
        self.image_width = 400
        self.image_height = 400

        # Resize image, remove if you want raw image size
        self.original_image = cv2.resize(self.original_image, (self.image_width, self.image_height))
        self.gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        self.clone = self.original_image.copy()

        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.extract_coordinates)

        self.image_coordinates = []
        self.extract = False

    def extract_coordinates(self, event, x, y, flags, parameters):
        # Record starting (x,y) coordinates on left mouse button click
        if event == cv2.EVENT_LBUTTONDOWN:
            self.image_coordinates = [(x,y)]
            self.extract = True

        # Record ending (x,y) coordintes on left mouse bottom release
        elif event == cv2.EVENT_LBUTTONUP:
            self.image_coordinates.append((x,y))
            self.extract = False

            # Draw rectangle around ROI
            cv2.rectangle(self.clone, self.image_coordinates[0], self.image_coordinates[1], (0,255,0), 2)
            self.draw_circle(self.image_coordinates[0], self.image_coordinates[1])
            # cv2.imshow("image", self.clone) 
        
        # Clear drawing boxes on right mouse button click
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.clone = self.original_image.copy()
    
    def draw_circle(self, top_left, bottom_right):
        ROI = self.gray[self.image_coordinates[0][1]:self.image_coordinates[1][1], self.image_coordinates[0][0]:self.image_coordinates[1][0]]
        
        try:
            circles = cv2.HoughCircles(ROI, cv2.HOUGH_GRADIENT, 1.2, 100)

            if circles is not None:
                circles = np.round(circles[0, :]).astype("int")

                for (x,y,r) in circles:
                    cv2.circle(self.clone, (x + top_left[0],y + top_left[1]), r, (0,255,0), 3)
        # No circles detected or unable to process image
        except cv2.error as e:
            pass

    def show_image(self):
        return self.clone

if __name__ == '__main__':
    extract_image_widget = DetectCirclesWidget()
    while True:
        cv2.imshow('image', extract_image_widget.show_image())
        key = cv2.waitKey(1)

        # Close program with keyboard 'q'
        if key == ord('q'):
            cv2.destroyAllWindows()
            exit(1)
