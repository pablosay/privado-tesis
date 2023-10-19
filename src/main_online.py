from online.apirequests import classify, detect, spoofdetect, register_entry, register_intruder

from utils.software import draw_bbox, draw_label, encode_image, is_hour_in_interval_vigilance, is_hour_past_vigilance, set_status, get_status

from utils.hardware.camera import extract_image_from_camera, camera_config
from utils.hardware.sensor import init_distance_sensor, measure_distance
from utils.hardware.display import init_display, disp_show_image, display_clear, display_show_spoof
from utils.hardware.light import init_light, turn_on, turn_off, accepted, denied

from picamera2 import Picamera2
import cv2
import argparse
import time
import RPi.GPIO as GPIO
from datetime import datetime

ip = None

blocked = False

def get_arguments():
	
	parser = argparse.ArgumentParser(description = 'Main online file: Makes api calls to the server.')
		
	parser.add_argument('ip', type = str, help ='IP of the backend')
		
	args = parser.parse_args()

	return args.ip
	
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
	
ip = get_arguments()

camera, disp, strip = init_configuration()

turn_off(strip)

display_clear(disp)

try:

	while True:
		
		while get_status() == "active":
					
			sensor_distance = measure_distance()
			
			if sensor_distance < 0.3:
				
				turn_on(strip)
				
				camera.start()
				
				end = time.time() + 10
				
				spoof_or_classification = False
				
				while True:
					
					countdown = get_countdown(end)
					
					if countdown > 0:
						
						if not spoof_or_classification:
						
							image = extract_image_from_camera(camera, (640,640))
					
							encoded_image = encode_image(image)
					
							facedetection_result = detect(encoded_image, ip)
					
							if facedetection_result['message'] == 'Successful':	
					
								for res in facedetection_result['result']:
									
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
														
														print("Welcome: ",classification['result'])
														
														draw_bbox(image, bbox)
														
														turn_off(strip)
														
														disp_show_image(disp, image)
														
														accepted(strip)
														
														spoof_or_classification = True
														
														entry_response = register_entry(classification['result'],  datetime.now())
														
														if entry_response["message"] == "Entry registed":
															
															print("Entry register")
														
														break
									
													elif i[5] == 0 and i[4] > 0.7:
														
														turn_off(strip)
									
														display_show_spoof(disp)
														
														denied(strip)
														
														spoof_or_classification = True
														
														intruder_response = register_intruder(classification['result'], datetime.now(), encoded_image)
														
														if intruder_response["message"] == "Intruder registed":
															
															print("Intruder register")
															
														if is_hour_in_interval_vigilance():
															
															print("Should block")
															
															set_status("blocked")
														
														break
									
													else: 
												
														print("Acercate mas a la camara")
										else:
											
											print("Desconocido")
						else:
							
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
				
		if is_hour_past_vigilance():
			
			set_status('active')
				
except Exception as e:
	
	print("ERROR: ", e)
	
finally:
	
	turn_off(strip)
	
	GPIO.cleanup()
	
	
    
