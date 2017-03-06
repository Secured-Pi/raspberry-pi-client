"""
This module contains code related to verification on the Raspberry-Pi.

The begin_watch function initializes the RFID scanner and webcam, then begins
looking for a face after an RFID is scanned.  Once a face is found, the
image is sent to the server to be validated. Some parts adapted from:
https://pythonprogramming.net/loading-video-python-opencv-tutorial/
"""

import cv2
import logging as log
import datetime as dt
import requests
import time
import os
from rfid import get_RFID


CASCADE_MODEL = 'haarcascade_frontalface_default.xml'
FACE_CASCADE = cv2.CascadeClassifier(CASCADE_MODEL)
log.basicConfig(filename='entries.log', level=log.INFO)
API_ENDPT = '/api/events/'
SERVER, PORT = 'http://192.168.1.109', '8000'   # Django server


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


def send_img_to_server(img_filename, server, port, rfid, username,
                       password):
    """Send a POST request to the main server.

    The request should contain the image, as well as the username and
    password for the user's account.
    """
    data = {
        'lock_id': '5',
        'serial': get_serial(),
        'RFID': rfid,
        'mtype': 'fr',
    }
    files = {'photo': open(img_filename, 'rb')}
    response = requests.post(server + ':' + port + API_ENDPT,
                             files=files, data=data,
                             auth=requests.auth.HTTPBasicAuth(username,
                                                              password))
    if response.status_code == 201:
        print('image sent to server for verification!')
        return(response)

    print('there was an error')
    print('status code: ', response.status_code)
    return response.reason


def begin_watch(server=SERVER, port=PORT, debug=False, username=None, password=None):
    """Begin watching the RFID scanner and camera for visitors.

    If a person's face is found, it is saved as a file and then sent off
    to the server to be validated.  When debug is True, the camera
    output is displayed on the screen.  Server and port are passed to the
    send_img_to_server function.
    """
    if not username or not password:
        print('No username/pw supplied!  Exiting.')
        return
    video_capture = cv2.VideoCapture(0)
    video_capture.set(3, 640)
    video_capture.set(4, 480)
    x = 0

    # TODO:  make the while loop continuous and not bug out, with RFID to
    # relock if the timer cannot be implemented well.
    while True:
        images_taken = 0
        rfid = get_RFID()

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
                send_img_to_server('testing.png', server, port, rfid, username, password)
                images_taken += 1
                log.info(str(dt.datetime.now()) + ' :: face found.')

            if debug:
                cv2.imshow('frame', gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # video_capture.release()  # causes a bug when enabled
        if debug:
            cv2.waitKey(1)
            cv2.destroyAllWindows()
            for i in range(5):
                cv2.waitKey(1)

if __name__ == '__main__':
    user = os.environ.get('LOCK_USER')
    password = os.environ.get('LOCK_PW')
    begin_watch(debug=True, username=user, password=password)
