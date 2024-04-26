import cv2

# Attempt to open the camera with the V4L2 backend explicitly specified
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Capture a frame to verify the camera is functioning
ret, frame = cap.read()
if not ret:
    print("Can't receive frame (stream end?). Exiting ...")
else:
    print("Frame captured successfully, dimensions: ", frame.shape)

cap.release()
