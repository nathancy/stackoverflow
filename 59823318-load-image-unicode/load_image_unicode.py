import cv2
import numpy as np
import glob

for path in glob.glob("images/*.jpg"):
    # Image is in BGR format
    image = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    cv2.imshow('image', image)
    cv2.waitKey(1000)

