# coding: utf-8
from socketIO_client import SocketIO
import pigpio


class RPiLock(object):
    """RPiLock class, a representation of the physical lock."""
    def __init__(self, server, port=80):
        """RPiLock instance with open socketio connection."""
        self.io_client = SocketIO(server, port)
        self.pi = pigpio.pi()
        self.avail_actions = {
            'unlock': 600,
            'lock': 2400,
        }

    def control(self, action, pin_num=18):
        """Output approriate control signal and pulswidth to the GPIO pins."""
        pulsewidth = self.avail_actions.get(action, None)
        if not pulsewidth:
            raise ValueError('Action not permitted')
        self.pi.set_servo_pulsewidth(pin_num, pulsewidth)
        return self.pi.get_servo_pulsewidth(pin_num)

    def listen_to_signal(self):
        """Establish a never-ending connection and listen to signal."""
        self.io_client.on('unlock', lambda x: self.control('unlock'))
        self.io_client.on('lock', lambda x: self.control('lock'))
        self.io_client.wait()
