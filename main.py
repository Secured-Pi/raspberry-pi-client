import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

p = GPIO.PWM(12, 50)

p.start(7.5)

try:
    while True:
        p.ChangeDutyCycle(7.5)
        time.sleep(0.25)
        p.ChangeDutyCycle(2.5)
        time.sleep(0.25)
        p.ChangeDutyCycle(12.5)
        time.sleep(0.25)
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
