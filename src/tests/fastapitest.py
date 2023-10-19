
import requests
from picamera2 import Picamera2
import cv2
import base64
import urllib3

urllib3.disable_warnings()

def encode_image(img):
	
	_, encoded_image = cv2.imencode('.jpg', img)
	
	base64_image = base64.b64encode(encoded_image).decode('utf-8')
	
	return base64_image

def detect(image):
	
	json_body_request = {'image': image}
	
	headers = {"Content-Type": "application/json"}
	
	response_classification = requests.post('https://192.168.1.22:1500/spoofdetect', json = json_body_request,  headers = headers, verify = False)
	
	return response_classification.json()
	

cam = Picamera2()
configuration = cam.create_preview_configuration(main={"size": (640, 640)}, controls={"FrameDurationLimits": (3333, 3333)})
cam.configure(configuration)
cam.start()

try:
    while True:
		
        im = cam.capture_array()
        
        rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        
        rgb = cv2.resize(rgb, (640,640))
        
        image = encode_image(rgb)
        
        result = detect(image)
        
        print(result)
 
except Exception as e:
	
	print("Error: ", str(e))
