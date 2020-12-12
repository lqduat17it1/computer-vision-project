import cv2
import numpy as np
from keras.models import load_model
model = load_model('pneumonia_v2.h5')

img = cv2.imread('normal.jpeg')

img = cv2.resize(img, (224, 224))
img = np.expand_dims(img, 0)
print(img.shape)
pred = model.predict(img)
pred = np.argmax(np.round(pred), axis=1)
print(pred[0])