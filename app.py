import cv2
import numpy as np
from keras.models import load_model
from flask import Flask, jsonify, request


app = Flask(__name__)
model = load_model('pneumonia_v2.h5')
data = {
  0: 'Normal',
  1: 'Pneumonia'
}

@app.route('/', methods=['POST']) 
def get_img():
  filestr = request.files['img'].read()
  img = np.frombuffer(filestr, np.uint8)
  img = cv2.imdecode(img, cv2.IMREAD_COLOR)
  img = cv2.resize(img, (224, 224))
  img = np.expand_dims(img, 0)
  pred = model.predict(img)
  pred = np.argmax(np.round(pred), axis=1)
  return jsonify({
    'message': data[pred[0]]
  })
  

@app.route('/api', methods=['GET'])
def get_tasks():
    return jsonify({
      'message': 'Hello Duật đao'
    })

if __name__ == '__main__':
    app.run(debug=True)