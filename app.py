from flask import Flask, Response
import cv2
import torch
import yolov5
from io import BytesIO
import base64
import numpy as np

app = Flask(__name__)

# Load the YOLOv5 model
model_path = "yolov5m.pt"
model = yolov5.load(model_path, device="cpu")
model.conf = 0.25  # Confidence threshold
model.iou = 0.45   # IOU threshold for NMS

def get_camera_frame():
    # Initialize the camera
    cap = cv2.VideoCapture(0)
    success, frame = cap.read()
    cap.release()
    if not success:
        return None
    return frame

def detect_persons(image):
    # Convert the color space from BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Perform inference
    results = model([image], size=640)
    # Draw bounding boxes for detected persons
    results = results.render()
    return results[0]

@app.route('/detect')
def detect():
    frame = get_camera_frame()
    if frame is None:
        return "Failed to capture image from camera", 400
    
    # Detect persons in the frame
    detected_image = detect_persons(frame)
    
    # Convert the color space from RGB back to BGR for correct color rendering
    detected_image = cv2.cvtColor(detected_image, cv2.COLOR_RGB2BGR)

    # Encode image for web display
    _, buffer = cv2.imencode('.jpg', detected_image)
    image_data = base64.b64encode(buffer).decode('utf-8')
    return Response(f'<img src="data:image/jpeg;base64,{image_data}" />', mimetype='text/html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
