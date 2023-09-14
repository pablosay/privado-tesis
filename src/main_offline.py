from offline.embedding_processing import get_face_embedding, get_known_embeddings
from offline.facepredictions import faceprediction
from offline.faceclassification import recognize
from offline.spoofdetection import spoofpredict
from utils.utils import draw_bbox, draw_label, extract_image_from_camera, camera_config, init_distance_sensor, measure_distance
from picamera2 import Picamera2
import cv2
import time

TRIG_PIN = 4  
ECHO_PIN = 17
wait_time = 10

print('Obteining known embeddings...')
known_embeddings = get_known_embeddings(['pablo', 'suzanne'])
print('Done.')

camera = Picamera2()

print('Initializing camera (Picamera2)...')
camera_config(camera)
print('Done.')

print('Initializing distance sensor...')
init_distance_sensor(TRIG_PIN, ECHO_PIN)
print('Done')


while True:
	
	print("Starting distance calculation")
	
	sensor_distance = measure_distance(TRIG_PIN,ECHO_PIN)
	
	if sensor_distance < 0.4:
		
		#Init camera
		
		camera.start()
		
		end = time.time() + wait_time
		
		while True:
			
			spoof_or_classification = False
			
			now = time.time()
                
			count = end - now
 
			if count > 0 and not spoof_or_classification:
	
				image = extract_image_from_camera(camera, (640,640))
				
				prediction = faceprediction(image)
				
				for result in prediction:
					
					bbox = result[:4]
						
					face_embedding = get_face_embedding(image, bbox, model = 'Facenet', spoof = False)
					
					predicted_name = recognize(face_embedding, known_embeddings)
					
					if predicted_name != 'unknown':
							
						x_min = int(bbox[0])
							
						y_min = int(bbox[1])
						
						spoof_prediction = spoofpredict(image)
						
						for i in spoof_prediction:
										
							if i[5] == 1 and i[4] > 0.8:
											
								draw_label(predicted_name, image, x_min, y_min)
								
								draw_bbox(image, bbox)
								
								spoof_or_classification = True
								
							elif i[5] == 0 and i[4] > 0.8:
								
								draw_label('Spoof', image, x_min, y_min)
								
								draw_bbox(image, bbox)
								
								spoof_or_classification = True
								
							else: 
										
								print("Acercate mas a la camara")
						
				cv2.imshow('Facial recognition', image)
					
				key = cv2.waitKey(1) & 0xFF
					
				if key == ord('q'):
					
					break
					
				if spoof_or_classification:
					
					print("Waiting to leave")
					time.sleep(5)
	
			else: 
				
				cv2.destroyAllWindows()
				
				break

		
		




