import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
from deepface import DeepFace
from ultralytics import YOLO

valid_extensions = ['.jpg', 'png']

facedetectionmodel = YOLO('best.pt')

known_embeddings_path = '../faces'


def extract_image(path, target_size):
	
	img = cv2.imread(path)
			
	img = cv2.resize(img, target_size)
			
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	
	return img
	
	
def extract_face(image, bbox):
	
	x_min, y_min, x_max, y_max = map(int, bbox)
		
	face = image[y_min:y_max, x_min:x_max]
	
	return face
	
	
def extract_face_embedding(image, bbox):
	
	x_min, y_min, x_max, y_max = map(int, bbox)
		
	face = image[y_min:y_max, x_min:x_max]
	
	embedding = DeepFace.represent(img_path = face, model_name = 'Facenet', enforce_detection = False)
	
	
	return embedding


def extract_known_embeddings_by_folderpath(path):
	
	embeddings = []
	
	for image in os.listdir(path):
		
		extension = image.split('.')[-1]
		
		if  extension in valid_extensions:
			
			filepath = path + '/' + image
			
			img = extract_image(filepath)
			
			facepredictions = facedetectionmodel(img, conf = 0.6, imgsz = 640, device = 'cpu')
			
			for result in facepredictions[0].boxes.data.numpy():
				
				bbox = result[:4]
				
				face_embedding = extract_face_embedding(img, bbox):
				
				embeddings.append(np.asarray(face_embedding[0]['embedding']))
				
	return embeddings
	
	
def get_embeddings(names):
	
	names_and_embeddings = []
	
	for name in names:
		
		embeddings = extract_known_embeddings_by_folderpath(known_embeddings_path + '/' + name)
		
		names_and_embeddings.append((name, embeddings))
		
	return names_and_embeddings
	
	
def euclidean_distance(x,y):
	
	return np.sqrt(np.sum((x-y) ** 2))
	
	
def compare_embeddings(reference, unknown, threshold):
	
	distances = []
	
	for embeding in reference:
		
		distances.append(euclidean_distance(embedding, unknown))
		
	distances = np.array(distances)
	
	return distances, list(distances <= threshold)
	

def draw_bbox(image, bbox):
	
	x_min, y_min, x_max, y_max = map(int, bbox)
	
	cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0,255,0), 2)
	

	
	
