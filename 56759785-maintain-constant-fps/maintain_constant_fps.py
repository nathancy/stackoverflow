import cv2
import time

cap = cv2.VideoCapture(0)

# Timeout to display frames in seconds
# FPS = 1/TIMEOUT 
# So 1/.025 = 40 FPS
TIMEOUT = 1
old_timestamp = time.time()

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if (time.time() - old_timestamp) > TIMEOUT:
        # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        print(old_timestamp)
        old_timestamp = time.time()

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
