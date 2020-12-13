import cv2
import numpy as np
from keras.models import load_model
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

model = load_model('pneumonia_v2.h5')
data = {
  0: 'Normal',
  1: 'Pneumonia'
}
  
@app.route('/', methods=['GET', 'POST'])
def home():
  if request.method == 'GET':
    return render_template('index.html')
  else:
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

if __name__ == '__main__':
  # print(app.config['STATIC_FOLDER'])
  app.run(debug=True)
