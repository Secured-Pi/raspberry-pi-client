#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock


class LockTestCase(unittest.TestCase):
    """Test the lock class."""
    def setUp(self):
        class Pi(object):
            def __init__(self):
                self.pulsewidth = 0

            def set_servo_pulsewidth(self, pin_num, pulsewidth):
                self.pulsewidth = pulsewidth

            def get_servo_pulsewidth(self, pin_num, pulsewidth):
                return self.pulsewidth

        modules = {
            'pigpio': MagicMock(),
            'pigpio.pi': Pi,
            'socketIO_client': MagicMock(),
        }
        self.fake_imports = patch.dict('sys.modules', modules)
        self.fake_imports.start()

    def tearDown(self):
        self.fake_imports.stop()

    def test_init_lock(self):
        """Test instantiate a RPiLock object."""
        from lock import RPiLock
        lock = RPiLock('localhost', 8000)
        self.assertTrue('lock' and 'unlock' in lock.avail_actions)

    def test_action_not_permitted(self):
        from lock import RPiLock
        lock = RPiLock('localhost', 8000)
        self.assertRaises(ValueError, lock.control, 'randomaction')

    def test_action_motorized_unlock(self):
        from lock import RPiLock
        lock = RPiLock('localhost', 8000)
        self.assertTrue(lock.control_motor('unlock'), 600)

    def test_action_motorized_lock(self):
        from lock import RPiLock
        lock = RPiLock('localhost', 8000)
        self.assertTrue(lock.control_motor('lock'), 2400)

if __name__ == '__main__':
    unittest.main()
