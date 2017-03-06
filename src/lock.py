# coding: utf-8
import requests

try:
    input = raw_input
except:
    pass

class RPiLock(object):
    """RPiLock class, a representation of the physical lock."""
    def __init__(self, user, server, port=80, model='motorized'):
        """RPiLock instance with socketio connection."""
        import pigpio
        self.user = user
        self.server, self.port = server, port
        self.model = model
        self.serial = self.get_serial()
        self.lock_id = self.get_lock_id()
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
                if 'Serial' in line[:6]:
                    serial = line[10:26]
        if not serial:
            raise IOError('Serial not found, make sure this is a RPi client')
        return serial

    def get_lock_id(self):
        print('Getting lock info...')
        req_url = 'http://{}:{}/api/locks/'.format(self.server, self.port)
        all_locks = requests.get(
            req_url,
            auth=requests.auth.HTTPBasicAuth(
                self.user.username,
                self.user.password,
            )
        ).json()
        for lock in all_locks:
            if lock['serial'] == self.serial:
                print('--DONE')
                print('lock pk:', lock['pk'])
                return lock['pk']
        else:
            print('NOT FOUND')
            print('Follow the prompt to register new lock:')
            print('Press CONTROL-C to quit at anytime')
            return self.self_register()

    def self_register(self):
        """Register a lock if it's not in user's lock list."""
        req_url = 'http://{}:{}/api/locks/'.format(
            self.server, self.port,
        )
        while True:
            name = input('Name (required): ')
            if name:
                break
        while True:
            location = input('Location (required): ')
            if location:
                break
        json = {
            'name': name,
            'location': location,
            'serial': self.serial,
            'active': True,
            'status': 'pending'
        }
        added_lock = requests.post(
            req_url,
            auth=requests.auth.HTTPBasicAuth(
                self.user.username,
                self.user.password
            ),
            json=json
        ).json()
        return added_lock['pk']

    def update_serverside_status(self, data):
        """Update lock status on central server."""
        lock_url = 'http://{}:{}/api/locks/{}/'.format(
            self.server, self.port, self.lock_id
        )
        event_url = 'http://{}:{}/api/events/{}/'.format(
            self.server, self.port, data['event_id']
        )
        return {
            'lock_res': requests.patch(
                            lock_url,
                            auth=requests.auth.HTTPBasicAuth(
                                self.user.username,
                                self.user.password
                            ),
                            json={'status': data['action'] + 'ed'},
                        ),
            'event_res': requests.patch(
                            event_url,
                            auth=requests.auth.HTTPBasicAuth(
                                self.user.username,
                                self.user.password
                            ),
                            json={'status': data['action'] + 'ed'},
                        )
        }

    def control_motorized(self, action, pin_num=18):
        """
        Output approriate motor control signal and pulswidth to the GPIO pins.
        """
        pulsewidth = self.avail_actions.get(action, None)
        if not pulsewidth:
            raise ValueError('Action not permitted')
        self.pi.set_servo_pulsewidth(pin_num, pulsewidth)
        return self.pi.get_servo_pulsewidth(pin_num)

    def control_electromagnetic(self, action):
        pass

    def handle_io_event(self, data):
        """Handling socketio event coming from server."""
        getattr(
            self,
            'control_{}'.format(self.model)
        )(data['action'])
        self.update_serverside_status({
            'action': data['action'], 'event_id': data['event_id']
        })

    def listen_for_io_signal(self, flask_port):
        """Establish a never-ending connection and listen to signal."""
        from socketIO_client import SocketIO
        print('server:', self.server, flask_port)
        self.io_client = SocketIO(self.server, flask_port)
        self.io_client.emit('listening', {'serial': self.serial})
        self.io_client.on('unlock', self.handle_io_event)
        self.io_client.on('lock', self.handle_io_event)
        print('Now listening to central server')
        self.io_client.wait()
