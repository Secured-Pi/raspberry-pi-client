#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from lock import RPiLock
from user import User
import sys
import logging
import getpass
logging.getLogger('socketIO-client').setLevel(logging.DEBUG)

# SERVER, PORT = '52.43.75.183', 8000     # Django server
SERVER, PORT = '192.168.1.109', 8000     # Django server, port
FLASK_PORT = 5000

try:
    input = raw_input
except:
    pass

def verify_user(server, port=PORT):
    """Verify a user."""
    while True:
        username = input('Secured Pi username: ')
        password = getpass.getpass()
        user = User(username, password, server, port)
        res = user.login()
        if res.status_code == 200:
            print('Secured Pi accepts you!')
            return user
        print('Can\'t authenticate')


def main():
    """Verify user, listen for instructions from server."""
    user = verify_user(SERVER, PORT)
    rpi_lock = RPiLock(user, SERVER, PORT)
    rpi_lock.listen_for_io_signal(FLASK_PORT)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nClient connection terminated.')
        sys.exit(0)
