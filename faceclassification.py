import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
from deepface import DeepFace
from ultralytics import YOLO
from picamera2 import Picamera2

valid_extensions = ['jpg', 'png']

facedetectionmodel = YOLO('best.pt')

known_embeddings_path = '../facenet'

names = ['pablo', 'suzanne']

camera = Picamera2()


def extract_image(path, target_size):
	
	img = cv2.imread(path)
			
	img = cv2.resize(img, target_size)
			
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	
	return img
	
	
def extract_image_from_camera(cam, target_size):
	
	im = cam.capture_array();
	
	rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
	
	rgb = cv2.resize(rgb, target_size)
	
	return rgb
	
	
def extract_face_embedding(image, bbox):
	
	x_min, y_min, x_max, y_max = map(int, bbox)
		
	face = image[y_min:y_max, x_min:x_max]
	
	face = cv2.resize(face, (160,160))
	
	embedding = DeepFace.represent(img_path = face, model_name = 'Facenet', enforce_detection = False)
	
	return np.asarray(embedding[0]['embedding'])


def list_known_embeddings_by_folderpath(path):
	
	embeddings = []
	
	for image in os.listdir(path):
		
		extension = image.split('.')[-1]
		
		if  extension in valid_extensions:
			
			filepath = path + '/' + image
			
			img = extract_image(filepath, (640,640))
			
			facepredictions = facedetectionmodel(img, conf = 0.6, imgsz = 640 ,device = 'cpu', verbose = False)
			
			for result in facepredictions[0].boxes.data.numpy():
				
				bbox = result[:4]
				
				face_embedding = extract_face_embedding(img, bbox)
				
				embeddings.append(face_embedding)
				
	return embeddings
	
	
def get_known_embeddings(names):
	
	names_and_embeddings = []
	
	for name in names:
		
		embeddings = list_known_embeddings_by_folderpath(known_embeddings_path + '/' + name)
		
		names_and_embeddings.append((name, embeddings))
		
	return names_and_embeddings
	
	
def euclidean_distance(x,y):
	
	return np.sqrt(np.sum((x-y) ** 2))
	
	
def compare_embeddings(reference, unknown, threshold):
	
	distances = []
	
	for embedding in reference:
		
		distances.append(euclidean_distance(embedding, unknown))
		
	distances = np.array(distances)
	
	return distances, list(distances <= threshold)
	
	
def recognize(unknown_embedding, knownembeds):
	
	for pair in knownembeds:
		
		name = pair[0]
		
		embeddings_by_name = pair[1]
		
		distances, recognition = compare_embeddings(embeddings_by_name, unknown_embedding, 10)
		
		if any(recognition):
			
			return name
	
	return 'unknown'
	

def draw_bbox(image, bbox):
	
	x_min, y_min, x_max, y_max = map(int, bbox)
	
	cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0,255,0), 2)
	

def draw_label(text, image, x_min, y_min):
	
	x_min, y_min, x_max, y_max = map(int, bbox)
	
	font = cv2.FONT_HERSHEY_SIMPLEX
	
	font_scale = 0.5
	
	font_thickness = 1
	
	text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
	
	text_height = y_min - 10
	
	cv2.putText(image, text, (x_min, text_height), font, font_scale, (0,255,0), font_thickness, lineType = cv2.LINE_AA)
	

def init_camera(cam):
	
	configuration = cam.create_preview_configuration(main={"size": (640, 640)}, controls={"FrameDurationLimits": (3333, 3333)})
	
	cam.configure(configuration)

	cam.start()
	

	
# Extract known embeddings
known_embeddings = get_known_embeddings(names)

init_camera(camera)

while True:
	
	image = extract_image_from_camera(camera, (640,640))
	
	prediction = facedetectionmodel(image, conf = 0.6, imgsz = 640 ,device = 'cpu', verbose = False)
	
	for result in prediction[0].boxes.data.numpy():
		
		prob = result[4]
		
		if prob > 0.6:
			
			bbox = result[:4]
			
			face_embedding = extract_face_embedding(image, bbox)
			
			predicted_name = recognize(face_embedding, known_embeddings)
				
			if predicted_name != 'unknown':
				
				draw_bbox(image, bbox)
				
				x_min = int(bbox[0])
				
				y_min = int(bbox[1])
				
				draw_label(predicted_name, image, x_min, y_min)
		
	cv2.imshow('Facial recognition', image)
		
	key = cv2.waitKey(1) & 0xFF
		
	if key == ord('q'):
		
		break
	
camera.stop()






	
	
	
	

	
	
	

	
	
