import cv2
import zmq
import base64
import numpy as np

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.bind('tcp://*:7777')
socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

while True:
    try:
        image_string = socket.recv_string()
        raw_image = base64.b64decode(image_string)
        image = np.frombuffer(raw_image, dtype=np.uint8)
        frame = cv2.imdecode(image, 1)
        cv2.imshow("frame", frame)
        cv2.waitKey(1)
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        break
