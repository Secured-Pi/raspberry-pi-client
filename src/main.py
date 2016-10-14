#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from lock import RPiLock
from user import User
import sys
import logging
import getpass
logging.getLogger('socketIO-client').setLevel(logging.DEBUG)

SERVER, PORT = '52.43.75.183', 8000


def verify_user(server, port=None):
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
    user = verify_user(SERVER, PORT)
    rpi_lock = RPiLock(user, SERVER, PORT)
    rpi_lock.listen_for_io_signal()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nClient connection terminated.')
        sys.exit(0)
