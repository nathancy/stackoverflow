import cv2

class ExtractArtworkROI(object):
    def __init__(self):
        # Load image
        self.original_image = cv2.imread('1.png')
        self.clone = self.original_image.copy()
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.extractROI)
        self.selected_ROI = False

        # ROI bounding box reference points
        self.image_coordinates = []

    def extractROI(self, event, x, y, flags, parameters):
        # Record starting (x,y) coordinates on left mouse button click
        if event == cv2.EVENT_LBUTTONDOWN:
            self.image_coordinates = [(x,y)]

        # Record ending (x,y) coordintes on left mouse button release
        elif event == cv2.EVENT_LBUTTONUP:
            # Remove old bounding box
            if self.selected_ROI:
                self.clone = self.original_image.copy()
                
            # Draw rectangle 
            self.selected_ROI = True
            self.image_coordinates.append((x,y))
            cv2.rectangle(self.clone, self.image_coordinates[0], self.image_coordinates[1], (36,255,12), 2)

            print('top left: {}, bottom right: {}'.format(self.image_coordinates[0], self.image_coordinates[1]))
            print('x,y,w,h : ({}, {}, {}, {})'.format(self.image_coordinates[0][0], self.image_coordinates[0][1], self.image_coordinates[1][0] - self.image_coordinates[0][0], self.image_coordinates[1][1] - self.image_coordinates[0][1]))

        # Clear drawing boxes on right mouse button click
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.selected_ROI = False
            self.clone = self.original_image.copy()

    def show_image(self):
        return self.clone
    
    def crop_ROI(self):
        if self.selected_ROI:
            x1 = self.image_coordinates[0][0]
            y1 = self.image_coordinates[0][1]
            x2 = self.image_coordinates[1][0]
            y2 = self.image_coordinates[1][1]
            
            # Extract ROI
            self.cropped_image = self.original_image.copy()[y1:y2, x1:x2]

            # Display and save image
            cv2.imshow('Cropped Image', self.cropped_image)
            cv2.imwrite('ROI.png', self.cropped_image)
        else:
            print('Select ROI before cropping!')

if __name__ == '__main__':
    extractArtworkROI = ExtractArtworkROI()
    while True:
        cv2.imshow('image', extractArtworkROI.show_image())
        key = cv2.waitKey(1)

        # Close program with keyboard 'q'
        if key == ord('q'):
            cv2.destroyAllWindows()
            exit(1)

        # Crop ROI
        if key == ord('c'):
            extractArtworkROI.crop_ROI()
