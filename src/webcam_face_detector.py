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

CASCADE_MODEL = 'haarcascade_frontalface_default.xml'
FACE_CASCADE = cv2.CascadeClassifier(CASCADE_MODEL)
log.basicConfig(filename='entries.log', level=log.INFO)
TOKEN = 'test-token'
SERVER, PORT = 'http://54.186.97.121', 8000
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


def send_img_to_server(img_filename, server, port, token):
    """Send a POST request to the main server.

    The request should contain the image, as well as a token.
    """
    data = {
        'lock_id': '4',
        'token': token,
        'serial': get_serial(),
        'RFID': '',
    }
    files = {'photo': open(img_filename, 'rb')}
    response = requests.post(server + ':' + str(PORT) + API_ENDPT,
                             files=files, data=data)

    if response.status_code == 201:
        print('image sent to server for verification!')
        return(response)
    else:
        print('there was an error')
        print('status code: ', response.status_code)
        return response.reason


def begin_watch(server=SERVER, port=PORT, token=TOKEN, debug=False):
    """Begin watching the camera for visitors.

    If a person's face is found, it is saved as a file and then send off
    to ther server to be validated.  When debug is True, the camera
    output is displayed on the screen.  Server, port, and token are passed
    to the send_img_to_server function.
    """
    video_capture = cv2.VideoCapture(0)
    video_capture.set(3, 640)
    video_capture.set(4, 480)
    num_faces_state = 0

    while True:
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

        # for logging
        # print(num_faces_state)
        if num_faces_state != len(faces):
            num_faces_state = len(faces)
            if num_faces_state == 1:
                time.sleep(1)
                cv2.imwrite('testing.png', gray)
                im = Image.open('testing.png')
                im.save('testing.gif')
                print('picture taken!')
                send_img_to_server('testing.gif', server, port, token)
                log.info(str(dt.datetime.now()) + ' :: face found.')

        if debug:
            cv2.imshow('Video', gray)

    video_capture.release()
    if debug:
        cv2.destroyAllWindows()

# if __name__ == '__main__':
#   begin_watch(debug=True)
