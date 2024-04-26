from flask import Flask, Response
import cv2
import torch
import numpy as np
import yolov5  # Ensure yolov5 is correctly installed and imported

app = Flask(__name__)

# Load YOLOv5 model
model = yolov5.load('yolov5m.pt')  # Adjust model path as necessary
model.conf = 0.25  # Set confidence threshold
model.iou = 0.45   # Set IoU threshold for NMS

def stream_frames():
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    if not cap.isOpened():
        print("Failed to open camera.")
        yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + open('error.jpg', 'rb').read() + b'\r\n'
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Frame capture failed, stopping.")
                break

            # Convert frame to RGB (YOLOv5 expects RGB)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Perform detection
            results = model([rgb_frame], size=640)  # Adjust size as needed
            # Render results on frame
            annotated_frame = results.render()[0]

            # Convert back to BGR for OpenCV
            annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)

            ret, jpeg = cv2.imencode('.jpg', annotated_frame)
            if not ret:
                continue
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n'
    finally:
        cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(stream_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, use_reloader=False)
