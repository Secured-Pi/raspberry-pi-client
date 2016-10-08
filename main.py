import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

while True:
    GPIO.setup(17, GPIO.OUT)
    print("LED on")
    time.sleep(1)
    GPIO.output(17, GPIO.LOW)
    print("LED off")
    time.sleep(1)
