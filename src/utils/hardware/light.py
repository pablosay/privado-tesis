from rpi_ws281x import Adafruit_NeoPixel, Color

def init_light():
	
	LED_COUNT = 35
	
	LED_PIN = 10
	    
	LED_FREQ_HZ = 800000
	  
	LED_DMA = 13
	  
	LED_BRIGHTNESS = 60
	  
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

def accepted(strip):
	
	for i in range(35):
		
		color = Color(0, 225, 0)  
		
		strip.setPixelColor(i, color)
    
	strip.show()
	
def denied(strip):
	
	for i in range(35):
		
		color = Color(225, 0, 0)  
		
		strip.setPixelColor(i, color)
    
	strip.show()
	
