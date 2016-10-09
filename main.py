# coding: utf-8
from lock import RPiLock

SERVER, PORT = '52.43.75.183', 8000


def main():
    rpi_lock = RPiLock(SERVER, PORT)
    rpi_lock.listen_to_signal()

if __name__ == '__main__':
    main()
