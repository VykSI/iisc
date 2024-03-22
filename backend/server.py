from flask import Flask, request, jsonify
import cv2
import numpy as np
from collections import Counter
import base64
from flask_cors import CORS,cross_origin

app = Flask(__name__)
cors = CORS(app)

# Load YOLO model and class labels
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
count = {}

with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Function to perform object detection and classification
def detect_and_classify_vehicle(image):
    global count
    count={}
    # Convert image to blob format
    blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    output_layers_names = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layers_names)

    # Initialization
    boxes = []
    confidences = []
    class_ids = []

    # Process detections
    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:  # Filter out weak detections
                # Get bounding box coordinates
                center_x = int(detection[0] * image.shape[1])
                center_y = int(detection[1] * image.shape[0])
                w = int(detection[2] * image.shape[1])
                h = int(detection[3] * image.shape[0])

                # Rectangle coordinates
                x = int(center_x - w/2)
                y = int(center_y - h/2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
                

    # Apply non-maximum suppression
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Draw bounding boxes and classify vehicles
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            try:
                    count[label] += 1
            except:
                    count[label] = 1
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(image, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return image

@app.route('/classify', methods=['POST'])
@cross_origin()
def classify_vehicle():
    # Check if an image is present in the request
    if 'image' not in request.files:
        return jsonify({'error': 'No image found in the request'}), 400

    # Read the image from the request
    image_file = request.files['image']
    image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_UNCHANGED)

    # Perform vehicle detection and classification
    classified_image = detect_and_classify_vehicle(image)

    # Reset count for new classification


    # Convert the resulting image to JPEG format
    _, jpeg_image = cv2.imencode('.jpg', classified_image)

    # Encode image bytes to base64
    base64_image = base64.b64encode(jpeg_image).decode('utf-8')

    # Return the classified image along with vehicle count
    return jsonify({'image': base64_image, 'count': count}), 200

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
