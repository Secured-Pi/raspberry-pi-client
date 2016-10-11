#!/usr/bin/python2
import serial
import re, sys, signal, os, time, datetime
import RPi.GPIO as GPIO
import MFRC522
from lock import RPiLock


CARDS = [
'18922217131215',
'5445101143241'
]
continue_reading = True
signal.signal(signal.SIGINT, end_read)
MIFAREReader = MFRC522.MFRC522()
lock = RPiLock('localhost', 8000)

def unlock_door(duration):
    if status == MIFAREReader.MI_OK and uid in CARDS:
        return lock.control('unlock'), 600)


# if __name__ == '__main__':
#     buffer = ''
#     ser = serial.Serial('/dev/ttyUSB0', BITRATE, timeout=0)
#     rfidPattern = re.compile(b'[\W_]+')
#     signal.signal(signal.SIGINT, signal_handler)
#
#     while True:
#       # Read data from RFID reader
#       buffer = buffer + ser.read(ser.inWaiting())
#       if '\n' in buffer:
#         lines = buffer.split('\n')
#         last_received = lines[-2]
#         match = rfidPattern.sub('', last_received)
#
#         if match:
#           print match
#           if match in CARDS:
#             print 'card authorized'
#             unlock_door(10)
#           else:
#             print 'unauthorized card'
#
#         # Clear buffer
#         buffer = ''
#         lines = ''
#
#       # Listen for Exit Button input
#       if not GPIO.input(3):
#         print "button pressed"
#         unlock_door(5)
#
#       time.sleep(0.1)
