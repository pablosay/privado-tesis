from picamera2 import Picamera2
import uuid
import time 

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (540, 540)}, controls={"FrameDurationLimits": (33333, 33333)}))
picam2.start_preview(True)
picam2.start()

for i in range(5): 
	
	(buffer, ), metadata = picam2.capture_buffers(["main"])
	
	img = picam2.helpers.make_image(buffer, picam2.camera_configuration()["main"])
	
	
	time.sleep(0.5)
	
picam2.stop()
	
