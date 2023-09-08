from offline.embedding_processing import get_face_embedding, get_known_embeddings
from offline.facepredictions import faceprediction
from offline.faceclassification import recognize
from utils.utils import draw_bbox, draw_label, extract_image_from_camera, init_camera
from picamera2 import Picamera2
import cv2
from skimage.feature import hog
from skimage import data, exposure
from ultralytics import YOLO
import numpy as np

def spoofprediction(image, model):
	
	prediction = model(image, conf = 0.75, imgsz = 640, verbose = False, device = 'cpu')
	
	if len(prediction) > 0:
		
		return prediction[0].boxes.data.numpy()
		
	return []
    
camera = Picamera2()
print('Initializing camera (Picamera2)...')
init_camera(camera)
print('Done.')

antispoofdetection = YOLO('antispoof.pt')

while True:
	
	image = extract_image_from_camera(camera, (640,640))
	
	prediction = faceprediction(image)
	
	if len(prediction) > 0:
		
		spoofpre = spoofprediction(image, antispoofdetection)
		
		for spoofresult in spoofpre:
			
			spoofbbox = spoofresult[:4]
			
			x_min, y_min = int(spoofbbox[0]), int(spoofbbox[1])
			
			if spoofresult[5] == 1 and spoofresult[4] > 0.8:
				
				draw_label('Live', image, x_min, y_min)
				
			elif spoofresult[5] == 0 and spoofresult[4] > 0.8:
				
				draw_label('spoof', image, x_min, y_min)
				
			else: 
				
				draw_label('indeciso', image, x_min, y_min)
				
			draw_bbox(image, spoofbbox)
			
	cv2.imshow('Anti spoof', image)
		
	key = cv2.waitKey(1) & 0xFF
		
	if key == ord('q'):
		
		break
	
camera.stop()
