from online.apirequests import classify, detect, spoofdetect, register_entry, register_intruder

from utils.software import draw_bbox, draw_label, encode_image, is_hour_in_interval_vigilance, is_hour_past_vigilance, set_status, get_status, send_message, concatenatedNameToSeparated

from utils.hardware.camera import extract_image_from_camera, camera_config
from utils.hardware.sensor import init_distance_sensor, measure_distance
from utils.hardware.display import init_display, disp_show_image, display_clear, display_show_text
from utils.hardware.light import init_light, turn_on, turn_off, accepted, denied, online_mode

from picamera2 import Picamera2
import cv2
import argparse
import time
import RPi.GPIO as GPIO
from datetime import datetime
from colorama import init, Fore, Back

ip = None

blocked = False

def get_arguments():
	
	parser = argparse.ArgumentParser(description = 'Main online file: Makes api calls to the server.')
		
	parser.add_argument('ip', type = str, help ='IP of the backend')
		
	args = parser.parse_args()

	return args.ip
	
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
	print('Done')
	
	print(Fore.BLUE + 'Initializing display...')
	disp = init_display()
	print('Done')
	
	print(Fore.BLUE + 'Initializing light...')
	strip = init_light()
	
	print('Done.')
	
	print("---------------------------------- \n")
	
	return camera, disp, strip
	
def get_countdown(end):
	
	now = time.time()
	
	return end - now
	
ip = get_arguments()

camera, disp, strip = init_configuration()

online_mode(strip)

display_clear(disp)

try:

	while True:
		
		while get_status() == "active":
					
			sensor_distance = measure_distance()
			
			if sensor_distance < 0.3:
				
				print(Fore.CYAN + "Object detected.")
				
				turn_on(strip)
				
				camera.start()
				
				end = time.time() + 10
				
				spoof_or_classification = False
				
				while True:
					
					countdown = get_countdown(end)
					
					if countdown > 0:
						
						if not spoof_or_classification:
						
							image = extract_image_from_camera(camera, (640,640))
							
							disp_show_image(disp, image)
					
							encoded_image = encode_image(image)
							
							timetodetect = time.time()
					
							facedetection_result = detect(encoded_image, ip)
					
							if facedetection_result['message'] == 'Successful':
					
								for res in facedetection_result['result']:
									
									print("Face detected.")
									
									bbox = res[:4]
							
									classification = classify(encoded_image, bbox, 'Facenet', ip)
							
									if classification['message'] == 'Successful':
							
										if classification['result'] != 'unknown':

											x_min = int(bbox[0])
										
											y_min = int(bbox[1])
									
											spoofresult = spoofdetect(encoded_image, ip)
									
											if spoofresult['message'] == 'Successful':
										
												for i in spoofresult['result']:
											
													if i[5] == 1: 
														
														print(Fore.YELLOW + "Face recognition time: ", time.time() - timetodetect)
												
														draw_label(classification['result'], image, x_min, y_min)
														
														print(Fore.GREEN + "Welcome: " + concatenatedNameToSeparated(classification['result']))
														
														draw_bbox(image, bbox)
														
														turn_off(strip)
														
														disp_show_image(disp, image)
														
														accepted(strip)
														
														spoof_or_classification = True
														
														entry_response = register_entry(classification['result'],  datetime.now())
														
														if entry_response["message"] == "Entry registed":
															
															
															send_message(concatenatedNameToSeparated(classification['result']) + " just entered.")

														else:
															
															print(entry_response["message"])
															
														break
														
													elif i[5] == 0:
																											
														turn_off(strip)
									
														display_show_text(disp, "Spoof",  36)
														
														denied(strip)
														
														spoof_or_classification = True
														
														intruder_response = register_intruder(classification['result'], datetime.now(), encoded_image)
														
														if intruder_response["message"] == "Intruder registed":
															
															print(Fore.RED + "Spoof detected with the face of " +concatenatedNameToSeparated(classification['result'])+ ".")
															
															send_message("Spoof detected with the face of " +concatenatedNameToSeparated(classification['result'])+ ".")
															
															pass
															
														if is_hour_in_interval_vigilance():
															
															send_message("Spoof detected with the face of " +concatenatedNameToSeparated(classification['result'])+ ". Device is blocked. It it is an error, you can activate the device on the configuration page.")
															
															print("Device is blocked")
															
															set_status("blocked")
														
														break
									
												if not any(spoofresult):
													
													print(Fore.YELLOW + "Couldnt determine if there was a spoof.")
												
										else:
											
											print(Fore.MAGENTA + "Unknown person.")
						else:
							
							time.sleep(5)
							
							turn_off(strip)
						
							camera.stop()
					
							display_clear(disp)
							
							break
							
					else:
						
						print(Fore.CYAN + "Expected time for recognition completed.")
						
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
	
	
    
