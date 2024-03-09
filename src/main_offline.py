from offline.embedding_processing import get_face_embedding, get_known_embeddings
from offline.facepredictions import faceprediction
from offline.faceclassification import recognize
from offline.spoofdetection import spoofpredict

from utils.hardware.camera import extract_image_from_camera, camera_config
from utils.hardware.sensor import init_distance_sensor, measure_distance
from utils.hardware.display import init_display, disp_show_image, display_clear, display_show_text
from utils.hardware.light import init_light, turn_on, turn_off, accepted, denied, offline_mode

from utils.software import draw_bbox, draw_label, get_ip, there_is_connection, check_internet_connection, concatenatedNameToSeparated

from picamera2 import Picamera2
import cv2
import time
import RPi.GPIO as GPIO
from colorama import init, Fore
import os

def init_configuration():
	
	print("----- Peripherals initializing-----")
	
	init(autoreset=True)
	
	GPIO.cleanup()
	
	camera = Picamera2()

	print(Fore.BLUE + 'Initializing camera (Picamera2)...')
	camera_config(camera)
	print('Done.')

	print(Fore.BLUE + 'Initializing distance sensor...')
	init_distance_sensor()
	print('Done.')
	
	print(Fore.BLUE + 'Initializing display...')
	disp = init_display()
	print('Done.')
	
	print(Fore.BLUE + 'Initializing light...')
	strip = init_light()

	print('Done.')
	
	print("---------------------------------- \n")
	
	return camera, disp, strip

def get_countdown(end):
	
	now = time.time()
	
	return end - now
	
camera, disp, strip = init_configuration()	

offline_mode(strip)

display_clear(disp)

print('Obtaining embeddings from folder ... ')

known_embeddings = get_known_embeddings(os.listdir("/home/pablosay21/Documentos/privado-tesis/data/classes"))

print('Done.')



try:
	
	while True:
		
		if check_internet_connection():
			
			print("There is internet connection.")
			
			if there_is_connection(get_ip()):
				
				break
				
			else:
				
				print("Processing server unreachable.")
				
		else:
			
			print("There is no internet connection.")
				
		sensor_distance = measure_distance()
		
		if sensor_distance < 0.3:
			
			print(Fore.CYAN + "Object detected.")
			
			turn_on(strip)
			
			camera.start()
			
			end = time.time() + 10
			
			spoof_or_classification = False
			
			while True:
				
				countdown = get_countdown(end)
				
				if countdown  > 0:
				
					if not spoof_or_classification:
						
						timetodetect = time.time()
			
						image = extract_image_from_camera(camera, (640,640))
						
						disp_show_image(disp, image)
						
						prediction = faceprediction(image)
						
						for result in prediction:
							
							print("Face detected.")
							
							bbox = result[:4]
							
							face_embedding = get_face_embedding(image, bbox, model = 'Facenet')
							
							predicted_name = recognize(face_embedding, known_embeddings)
							
							if predicted_name != 'unknown':
								
								x_min = int(bbox[0])
								
								y_min = int(bbox[1])
								
								spoof_prediction = spoofpredict(image)
								
								for i in spoof_prediction:
									
									if i[5] == 1:
										
										print(Fore.YELLOW + "Face recognition time: ", time.time() - timetodetect)
										
										print(Fore.GREEN + "Welcome: " + predicted_name)
										
										draw_label(predicted_name, image, x_min, y_min)
										
										draw_bbox(image, bbox)
										
										turn_off(strip)
										
										disp_show_image(disp, image)
										
										accepted(strip)
										
										spoof_or_classification = True
										
										break
										
									elif i[5] == 0:
										
										turn_off(strip)
										
										print(Fore.RED + "Spoof detected with the face of " + predicted_name  + ".")
										
										display_show_text(disp, "Spoof",  36)
										
										denied(strip)
										
										spoof_or_classification = True
										
										break
										
									else:
										
										print("Come near towards the camera.")
										
							else:
								
								print(Fore.MAGENTA + "Unknown person.")
					
					else:
						
						time.sleep(5)
						
						turn_off(strip)
					
						camera.stop()
				
						display_clear(disp)
						
						break
					
				else: 
					
					print(Fore.CYAN + "Expected time completed. ")
					
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
