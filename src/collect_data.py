from offline.facepredictions import faceprediction
from utils.utils import draw_bbox, draw_label, extract_image_from_camera, init_camera
from picamera2 import Picamera2
import cv2
import uuid

	
blurthres = 35
	
	
camera = Picamera2()

print('Initializing camera (Picamera2)...')
init_camera(camera)
print('Done.')

i = 0

while True:
	
	image = extract_image_from_camera(camera, (640,640))
	
	copy = image.copy()
	
	if i < 90:
		
		prediction = faceprediction(image)
		
		for result in prediction:
			
			bbox = result[:4]
			
			x_min = int(bbox[0])
					
			y_min = int(bbox[1])
			
			x_max = int(bbox[2])
			
			y_max = int(bbox[3])
			
			face = image[y_min:y_max, x_min:x_max]
			
			cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0,0,225), 2)
			
			blur_value = cv2.Laplacian(face, cv2.CV_64F).var()
			
			if blur_value > blurthres:
			
				filename = str(uuid.uuid4())
				
				output_filename = filename + '.jpg'
				
				cv2.imwrite('dataset/live/' + output_filename, copy)
				
				i = i + 1
	
	else:
		
		break
			

			
	cv2.imshow('Facial recognition', image)
		
	key = cv2.waitKey(1) & 0xFF
		
	if key == ord('q'):
		
		break
	
camera.stop()
		
