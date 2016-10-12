# coding: utf-8
import requests


class User(object):
    """User class, a representation of the Django user."""
    def __init__(self, username, password, server, port=80):
        self.server = server
        self.port = port
        self.username = username
        self.password = password

    def login(self):
        """Log in with provided username and password."""
        req_url = 'http://{}:{}/api/'.format(self.server, self.port)
        return requests.head(
            req_url,
            auth=requests.auth.HTTPBasicAuth(self.username, self.password)
        )
