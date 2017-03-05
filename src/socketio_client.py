# coding: utf-8
from socketIO_client import SocketIO
import pigpio

io_client = SocketIO('192.168.1.109', 5000)

AVAIL_ACTIONS = {
    'unlock': 600,
    'lock': 2400,
}


def lock_control(action, pin_num=18):
    """Output approriate control signal and pulswidth to the locl."""
    pi = pigpio.pi()
    pulsewidth = AVAIL_ACTIONS.get(action, None)
    if not pulsewidth:
        raise ValueError('Action not permitted')
    pi.set_servo_pulsewidth(pin_num, pulsewidth)
    return pi.get_servo_pulsewidth(pin_num)


io_client.on('unlock', lambda x: lock_control('unlock'))
io_client.on('lock', lambda x: lock_control('lock'))

if __name__ == '__main__':
    io_client.wait()
