import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(13,GPIO.OUT) #a

a = 1

GPIO.output(13, 1)
time.sleep(5)
GPIO.cleanup()