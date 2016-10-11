#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lock import RPiLock
import logging
logging.getLogger('socketIO-client').setLevel(logging.DEBUG)

SERVER, PORT = '52.43.75.183', 5000


def main():
    rpi_lock = RPiLock(SERVER, PORT)
    rpi_lock.listen_to_signal()

if __name__ == '__main__':
    main()
