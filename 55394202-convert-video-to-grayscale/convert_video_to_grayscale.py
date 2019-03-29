from threading import Thread
import cv2

class VideoToGrayscaleWidget(object):
    def __init__(self, src=0):
        # Create a VideoCapture object
        self.capture = cv2.VideoCapture(src)

        # Default resolutions of the frame are obtained (system dependent)
        self.frame_width = int(self.capture.get(3))
        self.frame_height = int(self.capture.get(4))

        # Set up codec and output video settings
        self.codec = cv2.VideoWriter_fourcc('M','J','P','G')
        self.output_video = cv2.VideoWriter('output.avi', self.codec, 30, (self.frame_width, self.frame_height), isColor=False)

        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()

    def show_frame(self):
        # Convert to grayscale and display frames
        if self.status:
            self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('grayscale frame', self.gray)

        # Press 'q' on keyboard to stop recording
        key = cv2.waitKey(1)
        if key == ord('q'):
            self.capture.release()
            self.output_video.release()
            cv2.destroyAllWindows()
            exit(1)

    def save_frame(self):
        # Save grayscale frame into video output file
        self.output_video.write(self.gray)

if __name__ == '__main__':
    video_src = '../assets/fedex.mp4'
    video_stream_widget = VideoToGrayscaleWidget(video_src)
    while True:
        try:
            video_stream_widget.show_frame()
            video_stream_widget.save_frame()
        except AttributeError:
            pass
