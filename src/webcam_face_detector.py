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
    from io import open
    serial = None
    with open('/proc/cpuinfo', 'r') as fh:
        for line in fh.readlines():
            if 'Serial' in line[0:6]:
                    serial = line[10:26]
    if not serial:
        raise IOError('Serial not found, make sure this is a RPi client')
    return serial


def send_img_to_server(img_filename='testing.gif', server=SERVER, port=PORT,
                       token=TOKEN):
    """Send a POST request to the main server.

    The request should contain the image, as well as a token.
    """
    # headers = {'X-Requested-With': 'Python requests', 'Content-type': 'image/gif'}
    with open('testing.gif', 'rb') as f:
        data = {
            'lock_id': '4',
            'token': token,
            'serial': 'testing123',
            'RFID': '',
            # 'photo': f,
        }
    files = {'photo': open('testing.gif', 'rb')}
    response = requests.post(server + ':' + str(PORT) + API_ENDPT,
                             files=files, data=data)

    if response.status_code == 201:
        print('image sent to server!')
        return(response)
    else:
        print('there was an error')
        print('status code: ', response.status_code)
        return response.reason


def begin_watch(debug=False):
    """Begin watching the camera for visitors.

    If a person's face is found, it is saved as a file and then send off
    to ther server to be validated.  When debug is True, the camera
    output is displayed on the screen.
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
                send_img_to_server('testing.gif', token=TOKEN)
                log.info(str(dt.datetime.now()) + ' :: face found.')

        if debug:
            cv2.imshow('Video', gray)   # black and white

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    if debug:
        cv2.destroyAllWindows()

# if __name__ == '__main__':
#   begin_watch(debug=True)
