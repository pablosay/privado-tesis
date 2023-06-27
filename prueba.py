import cv2
import time 

camera = cv2.VideoCapture(0)

if not camera.isOpened():
	raise ValueError("No se puede abrir la camara")
	
start_time = time.time()
	
while time.time() - start_time < 5:
	
	ret, frame = camera.read()
	
	cv2.imshow('Preview', frame)
	
	
camera.release()

cv2.destroyAllWindows()
