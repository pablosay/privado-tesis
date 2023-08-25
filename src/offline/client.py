from picamera2 import Picamera2
import base64
import requests
import cv2
import time

def draw_label(text, image, x_min, y_min):
	
	x_min, y_min, x_max, y_max = map(int, bbox)
	
	font = cv2.FONT_HERSHEY_SIMPLEX
	
	font_scale = 0.5
	
	font_thickness = 1
	
	text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
	
	text_height = y_min - 10
	
	cv2.putText(image, text, (x_min, text_height), font, font_scale, (0,255,0), font_thickness, lineType = cv2.LINE_AA)
	

picam2 = Picamera2()
confg = picam2.create_preview_configuration(main={"size": (640, 640)}, controls={"FrameDurationLimits": (3333, 3333)})
picam2.configure(confg)
picam2.start()


while True:
	
	im = picam2.capture_array();
	
	rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
	
	rgb = cv2.resize(rgb, (640,640))
	
	_, encoded_image = cv2.imencode('.jpg', rgb)
	
	base64_image = base64.b64encode(encoded_image).decode('utf-8')
	
	json_data = {'image': base64_image}
	
	response_prediction = requests.post('http://192.168.1.6:1500/predictface', json = json_data)
	
	result = response_prediction.json()
	
	for res in result['result']:
		
		bbox = res[:4]
		
		x_min, y_min, x_max, y_max = map(int, bbox)
		
		face = rgb[y_min:y_max, x_min:x_max]
		
		json_data2 = {'image': base64_image, 'bbox': bbox, 'model': 'Facenet'}
		
		response_class = requests.post('http://192.168.1.6:1500/classify', json = json_data2)
		
		classification = response_class.json()
		
		if classification['result'] != 'unknown':
			
			draw_label(classification['result'], rgb, x_min, y_min)
			
		cv2.rectangle(rgb, (x_min, y_min), (x_max, y_max), (0,255,0), 2)
	
	shape = str(rgb.shape)
		
	cv2.imshow('Prueba ' + shape, rgb)
	
	key = cv2.waitKey(1) & 0xFF
		
	if key == ord('q'):
		
		break
	
picam2.stop()
