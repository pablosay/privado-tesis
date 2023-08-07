from picamera2 import Picamera2, Preview
import time
import uuid

picam2 = Picamera2()
config = picam2.create_preview_configuration(main = {"size": (4000,4000)}, controls={"FrameDurationLimits": (16666, 16666)})
picam2.configure(config)
picam2.start_preview(True)
picam2.start()

for i in range(30):
		
	file_name = f'/home/pablosay21/Documentos/pablo/{str(uuid.uuid1())}.jpg'

	picam2.capture_file(file_name)
		
	time.sleep(0.5)
