from picamera2 import Picamera2
import time
import uuid
from rpi_ws281x import Adafruit_NeoPixel, Color

def init_light():
	
	LED_COUNT = 35
	
	LED_PIN = 10
	    
	LED_FREQ_HZ = 800000
	  
	LED_DMA = 13
	  
	LED_BRIGHTNESS = 70
	  
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

def capture_photos(num_photos):
	
	picam2 = Picamera2()
	camera_config = picam2.create_preview_configuration(main={"size": (3000, 3000)}, controls={"FrameDurationLimits": (3333, 3333)})
	picam2.configure(camera_config)
	picam2.start()
	
	for i in range(num_photos):
		
		file_name = f'/home/pablosay21/Documentos/data/{str(uuid.uuid1())}.jpg'

		picam2.capture_file(file_name)
		
		time.sleep(0.5)
		

print("hhol1")
strip = init_light()
strip.begin()
time.sleep(2)
print("hhol2")
turn_on(strip)
print("hhol3")
capture_photos(4)
print("hhol4")
turn_off(strip)



