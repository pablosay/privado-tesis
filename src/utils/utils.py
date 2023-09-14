import cv2
import base64
from picamera2 import Picamera2
import numpy as np
import RPi.GPIO as GPIO
import time

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
	
def extract_image_from_camera(cam, target_size):
	
	im = cam.capture_array();
	
	rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
	
	rgb = cv2.resize(rgb, target_size)
	
	return rgb

def camera_config(cam):
	
	configuration = cam.create_preview_configuration(main={"size": (640, 640)}, controls={"FrameDurationLimits": (3333, 3333)})
	
	cam.configure(configuration)

	cam.start()

def init_distance_sensor(TRIG_PIN, ECHO_PIN):
	
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(TRIG_PIN, GPIO.OUT)
	GPIO.setup(ECHO_PIN, GPIO.IN)
	
	
def measure_distance(TRIG_PIN, ECHO_PIN):
	
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.2)  

    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    speed_of_sound = 343.0 

    distance = (pulse_duration * speed_of_sound) / 2

    return distance
