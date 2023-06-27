from picamera2 import Picamera2
import time
import uuid

def capture_photos(num_photos):
	picam2 = Picamera2()
	camera_config = picam2.create_still_configuration()
	picam2.configure(camera_config)
	picam2.start()
	
	for i in range(num_photos):
		
		file_name = f'/home/pablosay21/Documentos/hd/{str(uuid.uuid1())}.jpg'

		picam2.capture_file(file_name)
		
		time.sleep(0.5)
		

capture_photos(30)

