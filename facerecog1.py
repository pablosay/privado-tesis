import time 
import cv2
from picamera2 import Picamera2
import numpy as np
from ultralytics import YOLO 

facerecognitionmodel = YOLO('frv8s.pt')

picam2 = Picamera2()
confg = picam2.create_preview_configuration(main={"size": (640, 640)})
picam2.configure(confg)
picam2.start()

while True:
	
	im = picam2.capture_array();
	
	rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
	
	rgb = cv2.resize(rgb, (640,640))
	
	facepredictions = facerecognitionmodel(rgb)
	
	for result in facepredictions[0].boxes.data.numpy():
		
		if(result[4] > 0.6): 
		
			bbox = result[:4]
			
			x_min, y_min, x_max, y_max = map(int, bbox)
			
			cv2.rectangle(rgb, (x_min, y_min), (x_max, y_max), (0,255,0), 2)
	
	shape = str(rgb.shape)
		
	cv2.imshow('Prueba ' + shape, rgb)
	
	key = cv2.waitKey(1) & 0xFF
		
	if key == ord('q'):
		
		break
	
picam2.stop()
	


