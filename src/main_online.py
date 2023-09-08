from utils.utils import draw_bbox, draw_label, extract_image_from_camera, init_camera, encode_image
from online.apirequests import classify, detect, spoofdetect
from picamera2 import Picamera2
import cv2
import argparse
import time

ip = None

parser = argparse.ArgumentParser(description = 'Main online file: Makes api calls to the server.')
	
parser.add_argument('ip', type = str, help ='IP of the backend')
	
args = parser.parse_args()

ip = args.ip

camera = Picamera2()

print('Initializing camera (Picamera2)...')
init_camera(camera)
print('Done.')

while True:
	
	image = extract_image_from_camera(camera, (640,640))
	
	encoded_image = encode_image(image)
	
	facedetection_result = detect(encoded_image, ip)
	
	if facedetection_result['message'] == 'Successful':	
	
		for res in facedetection_result['result']:
			
			spoofdetected = False
			
			bbox = res[:4]
			
			classification = classify(encoded_image, bbox, 'Facenet', ip)
			
			if classification['message'] == 'Successful':
			
				if classification['result'] != 'unknown':
					
					x_min = int(bbox[0])
						
					y_min = int(bbox[1])
					
					#Verifies only if there is a classify face
					
					spoofresult = spoofdetect(encoded_image, ip)
					
					if spoofresult['message'] == 'Successful':
						
						for i in spoofresult['result']:
							
							if i[5] == 1 and i[4] > 0.8:
								
								draw_label(classification['result'], image, x_min, y_min)
					
							elif i[5] == 0 and i[4] > 0.8:
					
								spoofdetected = True
					
							else: 
								
								print("Acercate mas a la camara")
								
						if spoofdetected:
							
							print("SPOOF DETECTED")
							
							break
				
			draw_bbox(image, bbox)
			
			
	
	shape = str(image.shape)
		
	cv2.imshow('Prueba ' + shape, image)
	
	key = cv2.waitKey(1) & 0xFF
		
	if key == ord('q'):
		
		break
	
camera.stop()
