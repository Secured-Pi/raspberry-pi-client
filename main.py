import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

while True:
    try:
        GPIO.output(17, GPIO.HIGH)
        print("LED on")
        time.sleep(1)
        GPIO.output(17, GPIO.LOW)
        print("LED off")
        time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
