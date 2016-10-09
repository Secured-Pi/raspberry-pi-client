# coding: utf-8
class RPiLock(object):
    """RPiLock class."""
    def __init__(self, pigio_instace, io_client):
        """RPiLock instance with open socketio connection."""
        self.io_client = io_client
        self.pi = pigio_instace
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
        for action in self.avail_actions:
            self.io_client.on(action, lambda x: self.lock_control(action))
