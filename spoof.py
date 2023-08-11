import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
from deepface import DeepFace
from ultralytics import YOLO
from picamera2 import Picamera2


spoofdetectionmodel = YOLO('../spoofdetection.pt')

facedetectionmodel = YOLO('best.pt')

for image in os.listdir('../hd'):
	
	img = cv2.imread('../hd/' + image)
	
	img = cv2.resize(img, (640,640))
	
	prediction = facedetectionmodel(img, conf = 0.6, imgsz = 640 ,device = 'cpu', verbose = False)
	
	for result in prediction[0].boxes.data.numpy():
		
		prob = result[4]
		
		if prob > 0.6:
			
			a = spoofdetectionmodel(img, imgsz = 640 ,device = 'cpu', verbose = False)
			
			for result in a:
				
				print(image + 'prob: ')
				print(result.probs.data[0])


