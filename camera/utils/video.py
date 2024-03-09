from picamera2 import Picamera2, Preview
import uuid
import time 

picam2 = Picamera2()
w =  640
h = 640
picam2.configure(picam2.create_preview_configuration(main={"size": (w, h)}, controls={"FrameDurationLimits": (33333, 33333)}))
picam2.start_preview(Preview.QTGL, width = w, height = h)
picam2.start()
time.sleep(5)
	
