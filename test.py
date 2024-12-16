import cv2
c = cv2.VideoCapture(0)
if not c.isOpened():
    print("Error: Cannot open video file")
else:
    print("Success")
c.release()