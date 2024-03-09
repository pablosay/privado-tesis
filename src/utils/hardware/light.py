import board
import neopixel
import time

def init_light():
	
	LED_COUNT = 35
	
	LED_PIN = board.D10
	
	LED_BRIGHTNESS = 0.8
	
	return neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness = LED_BRIGHTNESS, auto_write = False)

def turn_on(strip):
	
	color = (255, 255, 100)  
		
	strip.fill(color)
    
	strip.show()
	
def turn_off(strip):
		
	color = (0, 0, 0)  
		
	strip.fill(color)
    
	strip.show()

def accepted(strip):
		
	color = (0, 225, 0)
	
	strip.fill(color)
    
	strip.show()  

	
def denied(strip):
		
	color = (225,0,0)
	
	strip.fill(color)
    
	strip.show()
	
def online_mode(strip):
		
	color = (225,69,0)
		
	strip.fill(color)
		
	strip.show()
		
	time.sleep(5)
		
	color = (0,0,0)
		
	strip.fill(color)
		
	strip.show()

def offline_mode(strip):
		
	color = (88,2,125)
		
	strip.fill(color)
		
	strip.show()
		
	time.sleep(2)
		
	color = (0,0,0)
		
	strip.fill(color)
		
	strip.show()
