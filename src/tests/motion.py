import RPi.GPIO as GPIO
import time
from picamera2 import Picamera2
import cv2



GPIO.setmode(GPIO.BCM)
TRIG_PIN = 4  
ECHO_PIN = 17  
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
cam = Picamera2()
configuration = cam.create_preview_configuration(main={"size": (640, 640)}, controls={"FrameDurationLimits": (3333, 3333)})
cam.configure(configuration)
cam.start()

def measure_distance():
    # Ensure the trigger pin is low to start with
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.2)  # Allow for stabilization

    # Send a 10us trigger pulse
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    # Wait for the echo pin to go high (start of pulse)
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    # Wait for the echo pin to go low (end of pulse)
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    # Calculate the pulse duration
    pulse_duration = pulse_end - pulse_start

    # Speed of sound in air (in meters per second)
    speed_of_sound = 343.0  # meters per second

    # Calculate the distance (in meters)
    distance = (pulse_duration * speed_of_sound) / 2

    return distance

try:
    while True:
        
        distance = measure_distance()
        
        print(distance)
        
        if distance < 0.4:

            cam.start()
            
            end = time.time() + 5
            
            while True:
                
                now = time.time()
                
                res = end - now
                
                print(res)
                
                if res > 0:
                    
                    im = cam.capture_array();
	
                    rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
	
                    rgb = cv2.resize(rgb, (640,640))
                    
                    cv2.imshow('prev', rgb)
                    
                    key = cv2.waitKey(1) & 0xFF
		
                    if key == ord('q'):
		
                        break
                    
                else:
                    
                    cv2.destroyAllWindows()
                    
                    break
                    
            cam.stop()
 
except KeyboardInterrupt:
    GPIO.cleanup()
