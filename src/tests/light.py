'''
import time
from rpi_ws281x import Adafruit_NeoPixel, Color
import random 
LED_COUNT = 35  # Number of LEDs in your WS2812B strip
LED_PIN = 10    # GPIO pin connected to the data input of the WS2812B strip
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 5  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # Set True to invert the signal (when using NPN transistor level shift)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)

strip.begin()

while True:
    

    
    for i in range(LED_COUNT):
        
        color = Color(0, 0, 0)  
        
        strip.setPixelColor(i, color)
    
    strip.show()
    
    
    time.sleep(500)
    
    print("continue")
'''

import board
import neopixel
import time

LED_COUNT = 35
LED_PIN = board.D10
LED_BRIGHTNESS = 0.8

strip = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness = LED_BRIGHTNESS, auto_write = False)

try:
    
    while True:
        
        color = (225,225,168)
        strip.fill(color)
        strip.show()
        time.sleep(1)
        color = (0,0,0)
        strip.fill(color)
        strip.show()
        time.sleep(1)
    
except KeyboardInterrupt:
    
    strip.fill((0,0,0))
    strip.show()

