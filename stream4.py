from flask import Flask, Response
import cv2
import time
import yolov5  # Ensure yolov5 is correctly installed and imported

app = Flask(__name__)

# Load YOLOv5 model
model = yolov5.load('yolov5m.pt')  # Adjust model path as necessary
model.conf = 0.25  # Set confidence threshold
model.iou = 0.45   # Set IoU threshold for NMS

# Initialize a dictionary to hold count of detected attributes
people_count = {}

def stream_frames():
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    if not cap.isOpened():
        print("Failed to open camera.")
        yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + open('error.jpg', 'rb').read() + b'\r\n'
        return

    last_time = 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Frame capture failed, stopping.")
                break

            current_time = time.time()
            if current_time - last_time >= 1:  # Process the frame only every 1 second
                # Convert frame to RGB (YOLOv5 expects RGB)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Perform detection
                results = model([rgb_frame], size=640)  # Adjust size as needed
                detections = results.pred[0]
                
                # Resetting people count for each frame to get real-time count
                people_count.clear()
                
                # Process results
                for *box, conf, cls in detections:
                    if results.names[int(cls)] == 'person':
                        people_count['total'] = people_count.get('total', 0) + 1
                        # Assume other attributes (e.g., age, gender) could be parsed here
                        
                # Render results on frame
                frame = results.render()[0]
                last_time = current_time

            # Convert back to BGR for OpenCV
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n'
            # Optionally log people count
            print("Current people count:", people_count)
    finally:
        cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(stream_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, use_reloader=False)
