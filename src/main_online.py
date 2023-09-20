from utils.software import draw_bbox, draw_label, encode_image 
from utils.hardware.camera import extract_image_from_camera, camera_config
from utils.hardware.sensor import init_distance_sensor, measure_distance
from utils.hardware.display import init_display, disp_show_image, display_clear, display_show_spoof

from online.apirequests import classify, detect, spoofdetect
from picamera2 import Picamera2
import cv2
import argparse
import time
import RPi.GPIO as GPIO

ip = None


try:

	parser = argparse.ArgumentParser(description = 'Main online file: Makes api calls to the server.')
		
	parser.add_argument('ip', type = str, help ='IP of the backend')
		
	args = parser.parse_args()

	ip = args.ip

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

	while True:
		
		sensor_distance = measure_distance()
		
		if sensor_distance < 0.4:
			
			print("Distancia detectada") 
			
			camera.start()
			
			end = time.time() + 10
			
			spoof_or_classification = False
			
			while True:
				
				now = time.time()
					
				count = end - now
				
				if count > 0 and not spoof_or_classification:
				
					image = extract_image_from_camera(camera, (640,640))
			
					encoded_image = encode_image(image)
			
					facedetection_result = detect(encoded_image, ip)
			
					if facedetection_result['message'] == 'Successful':	
			
						for res in facedetection_result['result']:
							
							print("Detecto cara")
							
							bbox = res[:4]
					
							classification = classify(encoded_image, bbox, 'Facenet', ip)
					
							if classification['message'] == 'Successful':
					
								if classification['result'] != 'unknown':
							
									x_min = int(bbox[0])
								
									y_min = int(bbox[1])
							
									spoofresult = spoofdetect(encoded_image, ip)
							
									if spoofresult['message'] == 'Successful':
								
										for i in spoofresult['result']:
									
											if i[5] == 1 and i[4] > 0.7:
										
												draw_label(classification['result'], image, x_min, y_min)
												
												draw_bbox(image, bbox)
												
												disp_show_image(disp, image)
												
												spoof_or_classification = True
							
											elif i[5] == 0 and i[4] > 0.7:
							
												display_show_spoof(disp)
												
												spoof_or_classification = True
							
											else: 
										
												print("Acercate mas a la camara")
						
								else:
									
									print("Desconocido")
								
					if spoof_or_classification:
						
						print("Waiting to leave")
						
						time.sleep(10)
					
				else:
					
					print("Deteccion o cumplido tiempo de espera")
					
					print(count)
					
					break
	
			camera.stop()
			
			display_clear(disp)

except Exception as e:
	
	print(f"Error: {e}")
	
	
    
