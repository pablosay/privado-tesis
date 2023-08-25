from offline.embedding_processing import get_face_embedding, get_known_embeddings
from offline.facepredictions import faceprediction
from offline.faceclassification import recognize
from utils.utils import draw_bbox, draw_label, extract_image_from_camera, init_camera
from picamera2 import Picamera2
import cv2

print('Obteining known embeddings...')
known_embeddings = get_known_embeddings(['pablo', 'suzanne'])
print('Done.')

camera = Picamera2()

print('Initializing camera (Picamera2)...')
init_camera(camera)
print('Done.')

while True:
	
	image = extract_image_from_camera(camera, (640,640))
	
	prediction = faceprediction(image)
	
	for result in prediction:
		
		bbox = result[:4]
			
		face_embedding = get_face_embedding(image, bbox, model = 'Facenet', spoof = False)
		
		predicted_name = recognize(face_embedding, known_embeddings)
		
		if predicted_name != 'unknown':
				
			x_min = int(bbox[0])
				
			y_min = int(bbox[1])
				
			draw_label(predicted_name, image, x_min, y_min)
			
		draw_bbox(image, bbox)
			
	cv2.imshow('Facial recognition', image)
		
	key = cv2.waitKey(1) & 0xFF
		
	if key == ord('q'):
		
		break
	
camera.stop()
		
		




