import cv2
import numpy as np

class ExtractImageWidget(object):
    def __init__(self):
        self.original_image = cv2.imread('plane.PNG')

        # Resize image, remove if you want raw image size
        self.original_image = cv2.resize(self.original_image, (640, 556))
        self.clone = self.original_image.copy()

        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.extract_coordinates)

        # Bounding box reference points and boolean if we are extracting coordinates
        self.image_coordinates = []
        self.angle = 0
        self.extract = False
        self.selected_ROI = False

    def extract_coordinates(self, event, x, y, flags, parameters):
        # Record starting (x,y) coordinates on left mouse button click
        if event == cv2.EVENT_LBUTTONDOWN:
            self.image_coordinates = [(x,y)]
            self.extract = True

        # Record ending (x,y) coordintes on left mouse bottom release
        elif event == cv2.EVENT_LBUTTONUP:
            self.image_coordinates.append((x,y))
            self.extract = False
            
            self.selected_ROI = True
            self.crop_ROI()

            # Draw rectangle around ROI
            cv2.rectangle(self.clone, self.image_coordinates[0], self.image_coordinates[1], (0,255,0), 2)
            cv2.imshow("image", self.clone) 
        
        # Clear drawing boxes on right mouse button click and reset angle
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.clone = self.original_image.copy()
            self.angle = 0
            self.selected_ROI = False

    def show_image(self):
        return self.clone

    def rotate_image(self, angle):
        # Grab the dimensions of the image and then determine the center
        (h, w) = self.original_image.shape[:2]
        (cX, cY) = (w / 2, h / 2)
        
        self.angle += angle
        # grab the rotation matrix (applying the negative of the
        # angle to rotate clockwise), then grab the sine and cosine
        # (i.e., the rotation components of the matrix)
        M = cv2.getRotationMatrix2D((cX, cY), -self.angle, 1.0)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])

        # Compute the new bounding dimensions of the image
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))

        # Adjust the rotation matrix to take into account translation
        M[0, 2] += (nW / 2) - cX
        M[1, 2] += (nH / 2) - cY

        # Perform the actual rotation and return the image
        self.clone = cv2.warpAffine(self.original_image, M, (nW, nH))

        self.selected_ROI = False

    def crop_ROI(self):
        if self.selected_ROI:
            self.cropped_image = self.clone.copy()
                
            x1 = self.image_coordinates[0][0]
            y1 = self.image_coordinates[0][1]
            x2 = self.image_coordinates[1][0]
            y2 = self.image_coordinates[1][1]

            self.cropped_image = self.cropped_image[y1:y2, x1:x2]

            print('Cropped image: {} {}'.format(self.image_coordinates[0], self.image_coordinates[1]))
        else:
            print('Select ROI to crop before cropping')
    
    def show_cropped_ROI(self):
        cv2.imshow('cropped image', self.cropped_image)

if __name__ == '__main__':
    extract_image_widget = ExtractImageWidget()
    while True:
        cv2.imshow('image', extract_image_widget.show_image())
        key = cv2.waitKey(1)
        
        # Rotate clockwise 5 degrees
        if key == ord('r'):
            extract_image_widget.rotate_image(5)

        # Rotate counter clockwise 5 degrees
        if key == ord('e'):
            extract_image_widget.rotate_image(-5)
            
        # Close program with keyboard 'q'
        if key == ord('q'):
            cv2.destroyAllWindows()
            exit(1)
        
        # Crop image
        if key == ord('c'):
            extract_image_widget.show_cropped_ROI()

