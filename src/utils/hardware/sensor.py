import RPi.GPIO as GPIO
import time

TRIG_PIN = 4  
ECHO_PIN = 17
wait_time = 10

def init_distance_sensor():
	
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(TRIG_PIN, GPIO.OUT)
	GPIO.setup(ECHO_PIN, GPIO.IN)
	
	
def measure_distance():
	
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.2)  

    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    speed_of_sound = 343.0 

    distance = (pulse_duration * speed_of_sound) / 2

    return distance

