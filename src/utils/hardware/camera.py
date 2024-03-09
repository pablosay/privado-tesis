from picamera2 import Picamera2
import cv2

def extract_image_from_camera(cam, target_size):
	
	im = cam.capture_array();
	
	rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
	
	rgb = cv2.resize(rgb, target_size)
	
	return rgb

def camera_config(cam):
	
	configuration = cam.create_preview_configuration(main={"size": (640, 640)}, controls={"FrameDurationLimits": (33333, 33333)})
	
	cam.configure(configuration)

