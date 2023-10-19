from offline.embedding_processing import get_face_embedding, get_known_embeddings
from offline.facepredictions import faceprediction
from offline.faceclassification import recognize
from offline.spoofdetection import spoofpredict

from utils.hardware.camera import extract_image_from_camera, camera_config
from utils.hardware.sensor import init_distance_sensor, measure_distance
from utils.hardware.display import init_display, disp_show_image, display_clear, display_show_spoof
from utils.hardware.light import init_light, turn_on, turn_off, accepted, denied

from utils.software import draw_bbox, draw_label, get_ip, there_is_connection, check_internet_connection

from picamera2 import Picamera2
import cv2
import time
import RPi.GPIO as GPIO

def init_configuration():
	
	GPIO.cleanup()
	
	camera = Picamera2()

	print('Initializing camera (Picamera2)...')
	camera_config(camera)
	print('Done.')

	print('Initializing distance sensor...')
	init_distance_sensor()
	print('Done')
	
	print('Initializing display...')
	disp = init_display()
	print('Done')
	
	print('Initializing light...')
	strip = init_light()
	
	strip.begin()
	
	print('Done')
	
	return camera, disp, strip

def get_countdown(end):
	
	now = time.time()
	
	return end - now
	
known_embeddings = get_known_embeddings(['pablo',  'suzanne'])
	
camera, disp, strip = init_configuration()

turn_off(strip)

display_clear(disp)

try:

	while True:
		
		if check_internet_connection():
			
			print("There is internet connection")
			
			if there_is_connection(get_ip()):
				
				break
				
		sensor_distance = measure_distance()
		
		if sensor_distance < 0.3:
			
			print("Distancia detectada")
			
			turn_on(strip)
			
			camera.start()
			
			end = time.time() + 20
			
			spoof_or_classification = False
			
			while True:
				
				countdown = get_countdown(end)
				
				print(countdown)
				
				if countdown  > 0:
				
					if not spoof_or_classification:
						
						print("NO se ha detectado")
			
						image = extract_image_from_camera(camera, (640,640))
						
						prediction = faceprediction(image)
						
						for result in prediction:
							
							print("Cara detectada")
							
							bbox = result[:4]
							
							face_embedding = get_face_embedding(image, bbox, model = 'Facenet')
							
							predicted_name = recognize(face_embedding, known_embeddings)
							
							if predicted_name != 'unknown':
								
								x_min = int(bbox[0])
								
								y_min = int(bbox[1])
								
								spoof_prediction = spoofpredict(image)
								
								for i in spoof_prediction:
									
									if i[5] == 1 and i[4] > 0.7:
										
										draw_label(predicted_name, image, x_min, y_min)
										
										draw_bbox(image, bbox)
										
										turn_off(strip)
										
										disp_show_image(disp, image)
										
										accepted(strip)
										
										spoof_or_classification = True
										
										break
										
									elif i[5] == 0 and i[4] > 0.7:
										
										turn_off(strip)
										
										display_show_spoof(disp)
										
										denied(strip)
										
										spoof_or_classification = True
										
										break
										
									else:
										
										print("Acercate mas a la camara")
										
							else:
								
								print("Desconocido")
					
					else:
						
						print("Welcome! or get out")
						
						time.sleep(2)
						
						turn_off(strip)
					
						camera.stop()
				
						display_clear(disp)
						
						break
					
				else: 
					
					print("Tiempo de espera cumplido")
					
					turn_off(strip)
					
					camera.stop()
			
					display_clear(disp)
					
					break
			
			turn_off(strip)
			
			display_clear
			
		time.sleep(1)
		
except Exception as e:
	print("ERROR: ", e)
	
finally:
	GPIO.cleanup()
	turn_off(strip)
