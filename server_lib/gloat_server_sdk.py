import json

import requests


class GloatServerSDK:
    WHITE_LIST_URL = 'api/v1/users/whitelist'

    def __init__(self, client_id: str, client_secret: str, server: str = 'localhost', port: int = 5000):
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.server = server
        self.port = port

    def update_white_list(self, users_info: json):
        token = self.authenticate()
        url = f'http://{self.server}:{self.port}/{self.WHITE_LIST_URL}'
        data = {'token': token,
                'users_info': users_info}
        response = requests.get(url=url, json=data)
        return response

    def authenticate(self):
        pass
