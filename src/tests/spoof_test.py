from picamera2 import Picamera2
import cv2
from skimage.feature import hog
from skimage import data, exposure
from ultralytics import YOLO
import numpy as np

from rpi_ws281x import Adafruit_NeoPixel, Color

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
	
def extract_image_from_camera(cam, target_size):
	
	im = cam.capture_array();
	
	rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
	
	rgb = cv2.resize(rgb, target_size)
	
	return rgb

def init_light():
	
	LED_COUNT = 35
	
	LED_PIN = 10
	    
	LED_FREQ_HZ = 800000
	  
	LED_DMA = 13
	  
	LED_BRIGHTNESS = 40
	  
	LED_INVERT = False
	  
	return Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	
def turn_on(strip):
	
	for i in range(35):
		
		color = Color(255, 255, 100)  
		
		strip.setPixelColor(i, color)
    
	strip.show()
	
def turn_off(strip):
	
	for i in range(35):
		
		color = Color(0, 0, 0)  
		
		strip.setPixelColor(i, color)
    
	strip.show()

def spoofprediction(image, model):
	
	prediction = model(image, conf = 0.75, imgsz = 640, verbose = False, device = 'cpu')
	
	if len(prediction) > 0:
		
		return prediction[0].boxes.data.numpy()
		
	return []
	
def camera_config(cam):
	
	configuration = cam.create_preview_configuration(main={"size": (3000, 3000)}, controls={"FrameDurationLimits": (3333, 3333)})
	
	cam.configure(configuration)
    
camera = Picamera2()
print('Initializing camera (Picamera2)...')
camera_config(camera)
print('Done.')

strip  = init_light()

strip.begin()

turn_on(strip)

antispoofdetection = YOLO('antispoof.pt')

try:
	
	camera.start()
	
	while True:
		
		image = extract_image_from_camera(camera, (640,640))
		
		result = spoofprediction(image, antispoofdetection)
	
		for spoofresult in result:
				
			spoofbbox = spoofresult[:4]
				
			x_min, y_min = int(spoofbbox[0]), int(spoofbbox[1])
				
			if spoofresult[5] == 1 and spoofresult[4] > 0.8:
					
				draw_label('Live', image, x_min, y_min)
					
			elif spoofresult[5] == 0 and spoofresult[4] > 0.8:
					
				draw_label('spoof', image, x_min, y_min)
					
			else: 
					
				draw_label('indeciso', image, x_min, y_min)
					
			draw_bbox(image, spoofbbox)
				
		cv2.imshow('Anti spoof', image)
			
		key = cv2.waitKey(1) & 0xFF
			
		if key == ord('q'):
			
			turn_off(strip)
			
			break
		
except Exception as e:
	print("ERROR: ", e)
	
finally:
	turn_off(strip)
