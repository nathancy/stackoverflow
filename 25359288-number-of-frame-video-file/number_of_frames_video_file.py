def frame_count(video_path, manual=False):
    def manual_count(handler):
        frames = 0
        while True:
            status, frame = handler.read()
            if not status:
                break
            frames += 1
        return frames 

    cap = cv2.VideoCapture(video_path)
    # Slow, inefficient but 100% accurate method 
    if manual:
        frames = manual_count(cap)
    # Fast, efficient but inaccurate method
    else:
        try:
            frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        except:
            frames = manual_count(cap)
    cap.release()
    return frames

if __name__ == '__main__':
    import timeit
    import cv2

    start = timeit.default_timer()
    print('frames:', frame_count('fedex.mp4', manual=False))
    print(timeit.default_timer() - start, '(s)')

    start = timeit.default_timer()
    print('frames:', frame_count('fedex.mp4', manual=True))
    print(timeit.default_timer() - start, '(s)')
