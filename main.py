import time
from gpiozero import LED


led = LED(17)

while True:
    led.on()
    time.sleep(1)
    led.off()
    time.sleep(1)
