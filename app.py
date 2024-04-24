from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
from PIL import Image
import io

# Load the pre-trained image classification model
model = cv2.dnn.readNetFromONNX('model.onnx')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the uploaded image from the request
    img_file = request.files['image']
    
    # Read the image into a numpy array
    img_bytes = img_file.read()
    img_arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

    # Preprocess the image
    blob = cv2.dnn.blobFromImage(img, 1/255.0, (224, 224), swapRB=True, crop=False)

    # Set the input blob for the model
    model.setInput(blob)

    # Run inference and get the predictions
    preds = model.forward()

    # Get the top predicted class
    class_id = np.argmax(preds)

    # Return the predicted class as JSON response 
    return jsonify({'class_id': int(class_id)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
