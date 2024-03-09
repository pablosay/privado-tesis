

import board
import neopixel
import time

def offline_mode(strip):
    
    for i in range(3):
        
        color = (225,69,0)
        
        strip.fill(color)
        
        strip.show()
        
        time.sleep(10)
        
        color = (0,0,0)
        
        strip.fill(color)
        
        strip.show()
        
        time.sleep(0.3)

LED_COUNT = 35
LED_PIN = board.D10
LED_BRIGHTNESS = 0.2

strip = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness = LED_BRIGHTNESS, auto_write = False)


try:
    
    offline_mode(strip)
    
except KeyboardInterrupt:
    
    strip.fill((0,0,0))
    strip.show()

