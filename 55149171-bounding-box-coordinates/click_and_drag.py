import cv2

class ExtractImageWidget(object):
    def __init__(self):
        self.original_image = cv2.imread('placeholder.PNG')

        # Resize image, remove if you want raw image size
        self.original_image = cv2.resize(self.original_image, (640, 556))
        self.clone = self.original_image.copy()

        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.extract_coordinates)

        # Bounding box reference points and boolean if we are extracting coordinates
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
            print('top left: {}, bottom right: {}'.format(self.image_coordinates[0], self.image_coordinates[1]))

            # Draw rectangle around ROI
            cv2.rectangle(self.clone, self.image_coordinates[0], self.image_coordinates[1], (0,255,0), 2)
            cv2.imshow("image", self.clone) 
        
        # Clear drawing boxes on right mouse button click
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.clone = self.original_image.copy()

    def show_image(self):
        return self.clone

if __name__ == '__main__':
    extract_image_widget = ExtractImageWidget()
    while True:
        cv2.imshow('image', extract_image_widget.show_image())
        key = cv2.waitKey(1)

        # Close program with keyboard 'q'
        if key == ord('q'):
            cv2.destroyAllWindows()
            exit(1)
