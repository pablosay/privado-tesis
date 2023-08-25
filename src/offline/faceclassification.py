import os
import cv2
import numpy as np
from utils.utils import euclidean_distance

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
		
		distances, recognition = compare_embeddings(embeddings_by_name, unknown_embedding, 8)
		
		if any(recognition):
			
			return name
	
	return 'unknown'
