#!/usr/bin/python2
import MFRC522
import re, sys, signal, os, time, datetime
import RPi.GPIO as GPIO
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

def unlock_door():
    if status == MIFAREReader.MI_OK and uid in CARDS:
        return lock.control('unlock', 600)

