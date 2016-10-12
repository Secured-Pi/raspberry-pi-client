#!/usr/bin/python2
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
SERVER, PORT = 'http://54.186.97.121', 8000
API_ENDPT = '/api/locks/events'
lock = RPiLock(SERVER, PORT)

def get_serial(self):
    from io import open
    serial = None
    with open('/proc/cpuinfo', 'r') as fh:
        for line in fh.readlines():
            if 'Serial' in line[0:6]:
                serial = line[10:26]
    if not serial:
        raise IOError('Serial not found, make sure this is a RPi client')
    return serial
    

def send_rfid_to_server(uid, server=SERVER, port=PORT, token=TOKEN):
    """Send a POST request to the main server.

    The request should contain the image, as well as a token.
    """
    # TODO:
    # build/format the request to send to the Django server
    # include: img, token, serial, RFID
    data = {}
    data['lock_id']
    data['token'] = token
    data['serial'] = get_serial()
    data['RFID'] = uid

    with open('testing.gif', 'rb') as f:
        files = {'image': ('testing.gif', f, 'image/gif')}

    response = requests.post(server + ':' +str(PORT) + API_ENDPT, data=data, files=files)
    if response.status_code == 200:
        print('image sent to server!')
        return(response)
    else:
        print('there was an error')
        return response

def unlock_door(duration):
    if status == MIFAREReader.MI_OK and uid in CARDS:
        return lock.control('unlock', 600)


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
