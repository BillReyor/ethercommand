from flask import Flask, Response
import cv2

app = Flask(__name__)

def get_camera():
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    if not cap.isOpened():
        cap.release()
        raise Exception("Failed to open camera")
    return cap

def generate_frames(cap):
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    cap = get_camera()
    try:
        return Response(generate_frames(cap), mimetype='multipart/x-mixed-replace; boundary=frame')
    finally:
        cap.release()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, use_reloader=False)
