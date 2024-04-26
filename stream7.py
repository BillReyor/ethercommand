from flask import Flask, Response, render_template_string
import cv2
import time
import yolov5

app = Flask(__name__)

# Load YOLOv5 model
model = yolov5.load('yolov5m.pt')  # Adjust model path as necessary
model.conf = 0.25  # Set confidence threshold
model.iou = 0.45   # Set IoU threshold for NMS

# List to hold individual trackers and a set to track unique IDs
trackers = []
unique_ids = set()

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

def update_trackers(rgb_frame):
    global trackers
    for tracker in trackers[:]:
        success, _ = tracker.update(rgb_frame)
        if not success:
            trackers.remove(tracker)

def add_new_tracker(rgb_frame, box):
    tracker = cv2.TrackerKCF_create()
    tracker.init(rgb_frame, tuple(map(int, box)))
    trackers.append(tracker)

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

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = model([rgb_frame], size=640)
            detections = results.pred[0]

            update_trackers(rgb_frame)  # Update existing trackers

            # Add new trackers for new detections
            for *box, conf, cls_id in detections:
                if results.names[int(cls_id)] == 'person' and conf > 0.25:
                    add_new_tracker(rgb_frame, box)

            # Count unique people based on trackers
            unique_ids.update(trackers)

            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
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
    return {"total": len(unique_ids)}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, use_reloader=False)
