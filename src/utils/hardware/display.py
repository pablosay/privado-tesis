import board
import digitalio
from adafruit_rgb_display import st7735
import cv2
from PIL import Image, ImageDraw, ImageFont

height = 128

width = 160
	
def init_display():
	
	BAUDRATE = 24000000

	spi = board.SPI()
	
	reset_pin = digitalio.DigitalInOut(board.D26)  
	
	dc_pin = digitalio.DigitalInOut(board.D5)  
	
	cs_pin = digitalio.DigitalInOut(board.D6) 
	
	disp = st7735.ST7735R(spi, rotation=90, cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate = BAUDRATE)
	
	if disp.rotation % 180 == 90:
		
		height = disp.width 
		
		width = disp.height
		
	else:
		width = disp.width 
		
		height = disp.height
		
	return disp
	
		
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
		

def disp_show_image(disp, cv2image):
	
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
	
def display_show_spoof(disp):
	
	image = Image.new("RGB", (width, height), color=(255, 255, 255)) 

	draw = ImageDraw.Draw(image)

	draw.rectangle((0,0,width, height), outline = 0, fill = (0,0,0))

	text = "SPOOF"
	
	font = ImageFont.truetype("/usr/share/fonts/truetype/liberation2/LiberationMono-Bold.ttf", size=36)
	
	print(draw.textlength(text, font=font))
	
	text_length = draw.textlength(text, font=font)
	
	x = (width - int(text_length)) // 2
	
	y = (height - int(text_length)) // 2

	text_color = (225, 225, 225)
	
	draw.text((x, y), text, font=font, fill=text_color)
	
	disp.image(image)


