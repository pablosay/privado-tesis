import os
import cv2
import numpy as np
from offline.facepredictions import faceprediction
from deepface import DeepFace

known_faces_path = '/home/pablosay21/Documentos/privado-tesis/data/classes'

def extract_image(path, target_size):
	
	img = cv2.imread(path)
			
	img = cv2.resize(img, target_size)
			
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	
	return img
	
def get_face_embedding(image, bbox, model, spoof):

    x_min, y_min, x_max, y_max = map(int, bbox)
	
    face = image[y_min:y_max, x_min:x_max]

    if spoof == True:

        face = cv2.resize(face, (160, 160))

    embedding = DeepFace.represent(img_path = face, model_name = model, enforce_detection = False)

    return np.asarray(embedding[0]['embedding'])

def list_known_embeddings(knowfaces_path):
	
	embeddings = []
	
	for image in os.listdir(knowfaces_path):
			
		filepath = knowfaces_path + '/' + image
			
		img = extract_image(filepath, (640,640))
			
		pred = faceprediction(img)
			
		for result in pred:
				
			bbox = result[:4]
				
			face_embedding = get_face_embedding(img, bbox, model = 'Facenet', spoof = False)
				
			embeddings.append(face_embedding)
				
	return embeddings

def get_known_embeddings(names):
	
	names_and_embeddings = []
	
	for name in names:
		
		embeddings = list_known_embeddings(known_faces_path + '/' + name)
		
		names_and_embeddings.append((name, embeddings))
		
	return names_and_embeddings




	
	
