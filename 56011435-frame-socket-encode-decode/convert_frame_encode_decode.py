import cv2
import numpy as np

vid = cv2.VideoCapture(0)

while True:
    if vid.isOpened():
        empty, frame = vid.read()
        data = cv2.imencode('.jpg', frame)[1].tostring()

        # Intermediary socket stuffs

        nparr = np.fromstring(data, np.uint8)
        newFrame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2.imshow("s", newFrame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

vid.release()
