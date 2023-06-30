import time 
import cv2
from picamera2 import Picamera2
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np

def draw_rectange(image, x, y, w, h):
	
	cv2.rectangle(image, (x,y), (x + w, y + h), (0, 255, 0))
	
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
	tf.config.experimental.set_memory_growth(gpu, True)	
	
facetracker = load_model('facetracker3.h5')

cv2.startWindowThread()
picam2 = Picamera2()
confg = picam2.create_preview_configuration(main={"size": (2000, 2000), "format": "XRGB8888"})
picam2.configure(confg)
picam2.start()

while True:
	
	im = picam2.capture_array();
	
	im = cv2.resize(im, (600,600))
	
	rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
	
	resized = tf.image.resize(rgb, (120,120))
	
	yhat = facetracker.predict(np.expand_dims(resized/255, 0))
	
	sample_coords = yhat[1][0]
	
	
	if yhat[0] > 0.9:
		
		print("PAblo")
		
		cv2.rectangle(im, tuple(np.multiply(sample_coords[:2], [600, 600]).astype(int)), 
						  tuple(np.multiply(sample_coords[2:], [600, 600]).astype(int)),
						  (255,0,0), 2)
		
	cv2.imshow('Prueba', im)
	key = cv2.waitKey(1) & 0xFF
		
	if key == ord('q'):
		
		break
	
picam2.stop()
	


