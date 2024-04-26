from flask import Flask, Response, stream_with_context
import cv2
import torch
import yolov5
import base64

app = Flask(__name__)

# Load the YOLOv5 model
model_path = "yolov5m.pt"
model = yolov5.load(model_path, device="cpu")
model.conf = 0.25  # Confidence threshold
model.iou = 0.45   # IOU threshold for NMS

# Initialize the camera globally
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
if not cap.isOpened():
    print("Error: Could not open video device.")
    exit(1)

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            print("Failed to capture frame from camera. Check camera connectivity.")
            break

        # Process the frame
        frame = detect_persons(frame)

        # Encode the frame in JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_data = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')

def detect_persons(image):
    # Convert the color space from BGR to RGB for detection
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Perform inference
    results = model([image], size=640)
    # Draw bounding boxes for detected persons
    results = results.render()
    return cv2.cvtColor(results[0], cv2.COLOR_RGB2BGR)

@app.route('/video_feed')
def video_feed():
    # Use the generator function to stream video frames
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
