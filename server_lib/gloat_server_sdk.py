import json
import logging
import os

import requests
from requests.auth import HTTPBasicAuth


class GloatServerSDK:
    WHITE_LIST_URL = 'api/v1/users/whitelist'

    def __init__(self, client_id: str, client_secret: str, server: str = 'localhost', port: int = 5000):
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.server = server
        self.port = port
        self.client_id = 'ABCD'
        self.client_secret = os.environ.get('CLIENT_SECRET', 'GLOAT2020')
        self.url = f'http://{self.server}:{self.port}/{self.WHITE_LIST_URL}'

    # noinspection PyUnusedLocal
    def update_white_list(self, users_info: json):
        token = self.authenticate()
        if not token:
            logging.error('bad token')
        response = requests.post(f'{self.url}/users/whitelist',
                                 auth=HTTPBasicAuth(username=token, password='notused'))
        if response.status_code != 201:
            logging.error(f'bad status call for whitelist: {response.status_code=}')

    def authenticate(self):
        response = requests.get(f'{self.url}/token', auth=HTTPBasicAuth(username=self.client_id,
                                                                        password=self.client_secret))
        if response.status_code != 200:
            logging.error(f'bad status call for token: {response.status_code=}')
            return None
        token = response.json()['token']
        return token
