import cv2
import base64
import numpy as np
import requests
import urllib3
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime

urllib3.disable_warnings()

cred = credentials.Certificate('env/rtdb-pt23-firebase-adminsdk-xkgtx-1e365b35e5.json')

firebase_admin.initialize_app(cred, {
		'databaseURL': 'https://rtdb-pt23-default-rtdb.firebaseio.com'
	})
	
ref = db.reference('/device')

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
	
def get_vigilance_interval():
	
	start_time = datetime.strptime(ref.child('startinterval').get(), '%H:%M')
	
	end_time = datetime.strptime(ref.child('endinterval').get(), '%H:%M')
	
	return start_time, end_time
	
def get_ip():
	
	try:
		
		return ref.child('ip').get()
		
	except:
		
		return ""
		

def get_status():
	
	try:
		
		return ref.child('status').get()
		
	except:
		
		return "blocked"

def set_status(status):
	
	ref.child('status').set(status)

		
def there_is_connection(ip):
	
	if ip != "":
		
		try:
			
			print("Trying to reach processing server.")
		
			response = requests.get("https://"+ ip + ":1500/test", verify = False, timeout=2)
			
			return response.status_code == 200
		
		except:
			
			return False
			
	else:
		
		return False
	
def check_internet_connection(url='http://www.google.com', timeout=2):
	
	try:
		
		response = requests.get(url, timeout=timeout)
		
		return response.status_code == 200
		
	except requests.ConnectionError:
		
		return False

def is_hour_in_interval_vigilance():
	
	start_time, end_time = get_vigilance_interval()
	
	actual_time = datetime.now().strftime('%H:%M')
	
	actual_time = datetime.strptime(actual_time, '%H:%M')
	
	if start_time <= end_time:
		
		return start_time <= actual_time <= end_time
		
	else:
		
		return actual_time >= start_time or actual_time <= end_time
		

def is_hour_past_vigilance():
	
	_, end_time = get_vigilance_interval()
	
	actual_time = datetime.now().strftime('%H:%M')
	
	actual_time = datetime.strptime(actual_time, '%H:%M')
	
	return actual_time > end_time
	

