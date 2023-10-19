
import board
import digitalio
from adafruit_rgb_display import st7735
import time
import busio
import cv2
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw

height = 128

width = 160

def init_screen():
	
	BAUDRATE = 24000000

	spi = busio.SPI(clock = board.SCK_1, MOSI = board.MOSI_1)
	
	reset_pin = digitalio.DigitalInOut(board.D26)  
	
	dc_pin = digitalio.DigitalInOut(board.D5)  
	
	cs_pin = digitalio.DigitalInOut(board.D6) 
	
	return st7735.ST7735R(spi, rotation=270, cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate = BAUDRATE)
	
def config_screen_orientation(display, height, width):

	if disp.rotation % 180 == 90:
		
		height = disp.width 
		
		width = disp.height
		
	else:
		width = disp.width 
		
		height = disp.height
		
def scale_image(image):
	
	image_ratio = image.width / image.height
	
	screen_ratio = width / height
	
	if screen_ratio < image_ratio:
		
		scaled_width = image.width * height // image.height
		
		scaled_height = height

	else:
		
		scaled_width = width
    
		scaled_height = image.height * width // image.width
		
	image = image.resize((scaled_width, scaled_height), Image.BICUBIC)
	
	return image, scaled_width, scaled_height
		

def disp_show_image(disp, height, width, cv2image):
	
	image = Image.fromarray(cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGB))
	
	b, g, r = image.split()
	
	image = Image.merge("RGB", (r,g,b))
	
	image, scaled_width, scaled_height = scale_image(image)
	
	x = scaled_width // 2 - width // 2

	y = scaled_height // 2 - height // 2

	image = image.crop((x, y, x + width, y + height))
	
	disp.image(image)
	
def display_clear(disp):
	
	image = Image.new("RGB", (width, height))
	
	draw = ImageDraw.Draw(image)
	
	draw.rectangle((0,0,width, height), outline = 0, fill = (0,0,0))
	
	disp.image(image)
	
    
disp = init_screen()

config_screen_orientation(disp, height, width)

image = cv2.imread("prueba.jpg")

disp_show_image(disp, height, width, image)







