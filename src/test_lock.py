#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import json
from lock import RPiLock
from user import User
from requests import Response
try:
    from unittest.mock import patch, MagicMock, mock_open
except ImportError:
    from mock import patch, MagicMock, mock_open

FAKE_LOCKS = [
    {
        'pk': 1,
        'serial': 'randomserial',
    },
]


class LockTestCase(unittest.TestCase):
    """Test the lock class."""
    def setUp(self):
        class Pi(object):
            def __init__(self):
                self.pulsewidth = 0

            def set_servo_pulsewidth(self, pin_num, pulsewidth):
                self.pulsewidth = pulsewidth

            def get_servo_pulsewidth(self, pin_num):
                return self.pulsewidth

        modules = {
            'pigpio': MagicMock(),
            'socketIO_client': MagicMock(),
        }
        self.fake_imports = patch.dict('sys.modules', modules)
        self.fake_serial = patch(
            'io.open',
            new=mock_open(read_data="Serial:   randomserial"),
            create=True
        )
        mock_response = MagicMock(
            spec=Response,
            response=json.dumps(FAKE_LOCKS)
        )
        mock_response.json.return_value = FAKE_LOCKS
        self.fake_lock_id = patch(
            'requests.get',
            return_value=mock_response,
        )
        self.fake_imports.start()
        self.fake_serial.start()
        self.fake_lock_id.start()
        self.server = 'localhost'
        self.user = User('test_user', 'password', self.server)
        self.lock = RPiLock(self.user, self.server)
        self.lock.pi = Pi()

    def tearDown(self):
        self.fake_imports.stop()
        self.fake_serial.stop()
        self.fake_lock_id.stop()

    def test_init_lock(self):
        """Test instantiate a RPiLock object."""
        self.assertTrue('lock' and 'unlock' in self.lock.avail_actions)
        self.assertEqual(self.lock.model, 'motorized')
        self.assertEqual(self.lock.server, 'localhost')

    def test_get_serial(self):
        self.assertEqual(self.lock.serial, 'randomserial')

    def test_get_serverside_lock_id(self):
        self.assertEqual(self.lock.lock_id, 1)

    def test_action_not_permitted(self):
        self.assertRaises(ValueError, self.lock.control_motorized, 'action')

    def test_action_motorized_unlock(self):
        self.lock.control_motorized('unlock')
        self.assertEqual(self.lock.pi.get_servo_pulsewidth(18), 600)

    def test_action_motorized_lock(self):
        self.lock.control_motorized('lock')
        self.assertEqual(self.lock.pi.get_servo_pulsewidth(18), 2400)

    @patch(
        'requests.patch',
        return_value=MagicMock(
            spec=Response,
            response=json.dumps({'res': 'res'})
        ),
    )
    def test_update_serverside_status(self, req):
        data = {
            'event_id': 1,
            'action': 'lock'
        }
        res = self.lock.update_serverside_status(data)
        self.assertTrue('lock_res' and 'event_res' in res)

    @patch(
        'requests.post',
        return_value=MagicMock(
            spec=Response,
            response=json.dumps({'pk': 2})
        )
    )
    def test_self_register(self, req):
        self.assertTrue(self.lock.self_register(), 2)


if __name__ == '__main__':
    unittest.main()
