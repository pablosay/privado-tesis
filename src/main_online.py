from utils.utils import draw_bbox, draw_label, extract_image_from_camera, init_camera, encode_image
from online.apirequests import classify, detect
from picamera2 import Picamera2
import cv2

camera = Picamera2()

print('Initializing camera (Picamera2)...')
init_camera(camera)
print('Done.')

while True:
	
	image = extract_image_from_camera(camera, (640,640))
	
	encoded_image = encode_image(image)
	
	facedetection_result = detect(encoded_image)
	
	for res in facedetection_result['result']:
		
		bbox = res[:4]
		
		classification = classify(encoded_image, bbox, 'Facenet')
		
		if classification['result'] != 'unknown':
			
			x_min = int(bbox[0])
				
			y_min = int(bbox[1])
				
			draw_label(classification['result'], image, x_min, y_min)
			
		draw_bbox(image, bbox)
	
	shape = str(image.shape)
		
	cv2.imshow('Prueba ' + shape, image)
	
	key = cv2.waitKey(1) & 0xFF
		
	if key == ord('q'):
		
		break
	
camera.stop()
