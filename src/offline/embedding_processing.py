import os
import cv2
import numpy as np
from offline.facepredictions import faceprediction

known_faces_path = '../../data/classes/'

def extract_image(path, target_size):
	
	img = cv2.imread(path)
			
	img = cv2.resize(img, target_size)
			
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	
	return img




	
	
