"""
This module contains code related to the webcam on the Raspberry-Pi.

The begin_watch function initializes the webcam and begin looking for a
face.  Once a face is found, the image is sent to the server to be validated.
Some parts adapted from:
https://pythonprogramming.net/loading-video-python-opencv-tutorial/
"""

import cv2
import logging as log
import datetime as dt
from PIL import Image
import requests
import time
from rfid import get_RFID


CASCADE_MODEL = 'haarcascade_frontalface_default.xml'
FACE_CASCADE = cv2.CascadeClassifier(CASCADE_MODEL)
log.basicConfig(filename='entries.log', level=log.INFO)
TOKEN = 'test-token'
SERVER, PORT = 'http://54.186.97.121', 80
API_ENDPT = '/api/events/'


def get_serial():
    """Get serial number of Raspberry Pi."""
    from io import open
    serial = None
    with open('/proc/cpuinfo', 'r') as fh:
        for line in fh.readlines():
            if 'Serial' in line[0:6]:
                    serial = line[10:26]
    if not serial:
        raise IOError('Serial not found, make sure this is a RPi client')
    return serial


def send_img_to_server(img_filename, server, port, RFID, username='user100', password='user100password'):
    """Send a POST request to the main server.

    The request should contain the image, as well as a token.
    """
    data = {
        'lock_id': '4',
        'serial': 'testwsetset',
        'RFID': RFID,
        'mtype': 'fr',
    }
    auth=(username, password)
    files = {'photo': open(img_filename, 'rb')}
    response = requests.post(server + API_ENDPT,
                             files=files, data=data, auth=requests.auth.HTTPBasicAuth('user100','user100password'))
    if response.status_code == 201:
        print('image sent to server for verification!')
        return(response)
    else:
        import pdb;pdb.set_trace()
        print('there was an error')
        print('status code: ', response.status_code)
        return response.reason


def begin_watch(server=SERVER, port=PORT, debug=False):
    """Begin watching the camera for visitors.

    If a person's face is found, it is saved as a file and then send off
    to ther server to be validated.  When debug is True, the camera
    output is displayed on the screen.  Server, port, and token are passed
    to the send_img_to_server function.
    """
    RFID = get_RFID()
    video_capture = cv2.VideoCapture(0)
    video_capture.set(3, 640)
    video_capture.set(4, 480)
    num_faces_state = 0
    images_taken = 0

    while True:
        if images_taken > 5:
            break
    
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = FACE_CASCADE.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        if debug:
            for (x, y, w, h) in faces:
                cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if len(faces) == 1:
            time.sleep(1)
            cv2.imwrite('testing.png', gray)
            print('picture taken!')
            send_img_to_server('testing.png', server, port, RFID)
            images_taken += 1
            log.info(str(dt.datetime.now()) + ' :: face found.')
		
        if debug:
            cv2.imshow('frame', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
	
    video_capture.release()
    if debug:
        cv2.destroyAllWindows()

# if __name__ == '__main__':
#   begin_watch(debug=True)
