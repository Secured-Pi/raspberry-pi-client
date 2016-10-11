# coding: utf-8


class RPiLock(object):
    """RPiLock class, a representation of the physical lock."""
    def __init__(self, server, port):
        """RPiLock instance with socketio connection."""
        import pigpio
        self.serial = self.get_serial()
        self.server, self.port = server, port
        self.pi = pigpio.pi()
        self.avail_actions = {
            'unlock': 600,
            'lock': 2400,
        }

    def get_serial(self):
        """
        Get serial number on RPi, this need to be updated whenever new RPI
        model comes out.
        """
        from io import open
        serial = None
        with open('/proc/cpuinfo', 'r') as fh:
            for line in fh.readlines():
                if 'Serial' in line[0:6]:
                    serial = line[10:26]
        if not serial:
            raise IOError('Serial not found, make sure this is a RPi client')
        return serial

    def update_serverside_status(self, data):
        """Update lock status on central server."""
        import requests
        req_url = 'http://{}:{}/api/locks/{}'.format(
            self.server, self.port, data['lock_id']
        )
        return requests.post(req_url, json=data)

    def handle_io_event(self, data):
        """Handling socketio event coming from server."""
        pass

    def control(self, action, pin_num=18):
        """Output approriate control signal and pulswidth to the GPIO pins."""
        pulsewidth = self.avail_actions.get(action, None)
        if not pulsewidth:
            raise ValueError('Action not permitted')
        self.pi.set_servo_pulsewidth(pin_num, pulsewidth)
        return self.pi.get_servo_pulsewidth(pin_num)

    def io_connect(self):
        """Connect to socketio server."""
        from socketIO_client import SocketIO
        self.io_client = SocketIO(self.server, self.port)
        self.io_client.emit('listening', {'serial': self.serial})

    def listen_to_signal(self):
        """Establish a never-ending connection and listen to signal."""
        self.io_client.on('unlock', lambda x: self.control('unlock'))
        self.io_client.on('lock', lambda x: self.control('lock'))
        self.io_client.wait()
