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
import Image
import requests

CASCADE_MODEL = 'haarcascade_frontalface_default.xml'
FACE_CASCADE = cv2.CascadeClassifier(CASCADE_MODEL)
log.basicConfig(filename='entries.log', level=log.INFO)
TOKEN = 'test-token'
SERVER, PORT = '52.43.75.183', 8000


def send_img_to_server(img_filename, server=SERVER, port=PORT, token=TOKEN):
    """Send a post request to the main server.

    The request should contain the image, as well as a token.
    """
    print('image sent to server!')
    pass


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
                cv2.imwrite('testing.png', gray)
                im = Image.open('testing.png')
                im.save('testing.gif')
                print('picture taken!')
                send_img_to_server('testing.gif')
                log.info(str(dt.datetime.now()) + '::face found.')

        if debug:
            cv2.imshow('Video', gray)   # black and white

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    if debug:
        cv2.destroyAllWindows()
