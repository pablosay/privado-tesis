from picamera2 import Picamera2, Preview
import time
import uuid

picam2 = Picamera2()
config = picam2.create_preview_configuration()
picam2.configure(config)
picam2.start_preview(True)
picam2.start()

for i in range(30):
		
	file_name = f'/home/pablosay21/Documentos/lofi/{str(uuid.uuid1())}.jpg'

	#picam2.capture_file(file_name)
		
	time.sleep(0.5)
