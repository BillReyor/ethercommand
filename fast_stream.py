from flask import Flask, Response, render_template_string
import cv2
import time
import yolov5  # Make sure yolov5 is installed and accessible

app = Flask(__name__)

# Load YOLOv5 model
model = yolov5.load('yolov5s.pt')  # Adjust model path as necessary
model.conf = 0.35  # Set confidence threshold
model.iou = 0.5    # Set IoU threshold for NMS

# Global variable to hold count of detected attributes
people_count = {'total': 0}

# HTML Template for serving the video feed and stats
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Live Object Detection</title>
    <style>
        body { display: flex; justify-content: center; align-items: center; flex-direction: column; }
        #stats { margin-top: 20px; }
    </style>
</head>
<body>
    <img src="{{ url_for('video_feed') }}" width="640" height="480" alt="Video Feed">
    <div id="stats">People detected: 0</div>
    <script>
        setInterval(function() {
            fetch("/stats")
            .then(response => response.json())
            .then(data => {
                document.getElementById("stats").innerHTML = "People detected: " + data.total;
            });
        }, 1000);  // Update the stats every second
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

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
            if current_time - last_time >= 0.5:  # Process the frame every 0.5 seconds
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = model([rgb_frame], size=640)
                detections = results.pred[0]
                
                # Update global count
                people_count['total'] = sum(1 for *_, cls in detections if results.names[int(cls)] == 'person')
                
                # Render detections directly onto the frame
                for *xyxy, conf, cls in detections:
                    label = f'{results.names[int(cls)]} {conf:.2f}'
                    cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (255, 0, 0), 2)
                    cv2.putText(frame, label, (int(xyxy[0]), int(xyxy[1])-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                last_time = current_time

            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n'
    finally:
        cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(stream_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stats')
def stats():
    return {"total": people_count.get('total', 0)}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, use_reloader=False)
