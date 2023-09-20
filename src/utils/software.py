import cv2
import base64
import numpy as np

def draw_bbox(image, bbox):
	
	x_min, y_min, x_max, y_max = map(int, bbox)
	
	cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0,255,0), 2)
	

def draw_label(text, image, x_min, y_min):
	
	font = cv2.FONT_HERSHEY_SIMPLEX
	
	font_scale = 0.5
	
	font_thickness = 1
	
	text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
	
	text_height = y_min - 10
	
	cv2.putText(image, text, (x_min, text_height), font, font_scale, (0,255,0), font_thickness, lineType = cv2.LINE_AA)
	
def encode_image(img):
	
	_, encoded_image = cv2.imencode('.jpg', img)
	
	base64_image = base64.b64encode(encoded_image).decode('utf-8')
	
	return base64_image
	
def euclidean_distance(x,y):
	
	return np.sqrt(np.sum((x-y) ** 2))

