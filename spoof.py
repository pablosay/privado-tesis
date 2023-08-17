import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
from ultralytics import YOLO
import tensorflow as tf
from deepface import DeepFace
import joblib
import threading
import concurrent.futures

def get_emebedding(image):
	
	return DeepFace.represent(img_path = image, model_name = 'Facenet', enforce_detection = False)
	
def get_denoised_ycrcb(denoised):
	
	return cv2.cvtColor(denoised, cv2.COLOR_RGB2YCrCb)
	
	
def get_denoised_luv(denoised):
	
	return cv2.cvtColor(denoised_image, cv2.COLOR_RGB2Luv)
	
	

from picamera2 import Picamera2

facerecognitionmodel = YOLO('best.pt')

spoofmodel = joblib.load('svm_model_facenet.joblib')

picam2 = Picamera2()
confg = picam2.create_preview_configuration(main={"size": (2000, 2000)}, controls={"FrameDurationLimits": (3333, 3333)})
picam2.configure(confg)
picam2.start()

while True:
	
	im = picam2.capture_array();
	
	rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
	
	rgb = cv2.resize(rgb, (640,640))
	
	start = time.time()
	
	facepredictions = facerecognitionmodel(rgb, conf = 0.6,imgsz = 640, device = 'cpu', verbose = False)
	
	for result in facepredictions[0].boxes.data.numpy():
		
		bbox = result[:4]
		
		x_min, y_min, x_max, y_max = map(int, bbox)
		
		face = rgb[y_min:y_max, x_min:x_max]
		
		denoised_image = cv2.fastNlMeansDenoising(face, None, h = 10, searchWindowSize = 21, templateWindowSize = 7)
		
		denoised_ycrcb = get_denoised_ycrcb(denoised_image)
		
		denoised_luv = get_denoised_ycrcb(denoised_image)
		
		ycrcb_embedding = get_emebedding(denoised_ycrcb)
		
		luv_embedding = get_emebedding(denoised_luv)
		
		joined = np.concatenate((ycrcb_embedding[0]['embedding'], luv_embedding[0]['embedding']))
		
		'''
		with concurrent.futures.ThreadPoolExecutor(max_workers = 2) as executor:
			
			denoised_ycrcb = executor.submit(get_denoised_ycrcb, denoised_image)
			
			denoised_luv = executor.submit(get_denoised_ycrcb, denoised_image)
			
		completed = concurrent.futures.wait([denoised_ycrcb, denoised_luv], return_when = concurrent.futures.ALL_COMPLETED).done
			
		denoised_ycrcb_result, denoised_luv_result = [future.result() for future in completed]
		
		
		with concurrent.futures.ThreadPoolExecutor(max_workers = 2) as executor:
			
		
			ycrcb_embedding = executor.submit(get_emebedding, denoised_ycrcb_result)
			
			luv_embedding =  executor.submit(get_emebedding, denoised_luv_result)
			
		completed = concurrent.futures.wait([ycrcb_embedding, luv_embedding], return_when = concurrent.futures.ALL_COMPLETED).done
			
		ycrcb_embedding_result, luv_embedding_result = [future.result() for future in completed]
		
		joined = np.concatenate((ycrcb_embedding_result[0]['embedding'], luv_embedding_result[0]['embedding']))
		'''
		
		sample = np.expand_dims(joined, axis = 0)
		
		result = spoofmodel.predict_proba(sample)
		
		print(result[0][1])
		
		'''
			
		if result[0] == 1:
			
			print('Alive')
			print(result)
			
			cv2.rectangle(rgb, (x_min, y_min), (x_max, y_max), (0,255,0), 2)
			
		else:
			
			print('Fake')
			
			cv2.rectangle(rgb, (x_min, y_min), (x_max, y_max), (225,0,0), 2) 
		
		'''
			
	end = time.time()
	
	total = end - start
	
	print("Excecution Time: ",total, "seconds")
	
	shape = str(rgb.shape)
		
	cv2.imshow('Prueba ' + shape, rgb)
	
	key = cv2.waitKey(1) & 0xFF
		
	if key == ord('q'):
		
		break
	
picam2.stop()




