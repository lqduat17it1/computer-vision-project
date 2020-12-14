import cv2
import numpy as np
import json
from tflite_runtime.interpreter import Interpreter
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

interpreter = Interpreter('model_lite.tflite')
interpreter.allocate_tensors()

with open('labels.json') as f:
  data = json.load(f)

def allowed_file(filename):
  extension = filename.rsplit('.', 1)[1].lower()
  return '.' in filename and extension in ALLOWED_EXTENSIONS
  
@app.route('/', methods=['GET', 'POST'])
def home():
  if request.method == 'GET':
    return render_template('index.html')
  else:
    if 'img' not in request.files:
      return jsonify({
        'message': 'Missing file'
      }), 400
    file = request.files['img']
    if file.filename == '':
      return jsonify({
        'message': 'No file selected'
      }), 400
    
    if file and allowed_file(file.filename):
      try:
        filestr = file.read()
        img = np.frombuffer(filestr, np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        img = cv2.resize(img, (224, 224))
        img = np.expand_dims(img, 0)
        input_tensor = img.astype('float32')

        input_index = interpreter.get_input_details()[0]['index']
        interpreter.set_tensor(input_index, input_tensor)
        interpreter.invoke()
        output_details = interpreter.get_output_details()[0]
        output = np.squeeze(interpreter.get_tensor(output_details['index']))
        pred = np.argmax(np.round(output))
        return jsonify({
          'message': data[str(pred)]
        })
      except Exception as e:
        print(e)
        return jsonify({
          'message': 'Server error'
        }), 500
    else:
      return jsonify({
        'message': 'File doesnt support'
      }), 400
