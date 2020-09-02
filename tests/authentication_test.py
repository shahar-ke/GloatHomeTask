from unittest import TestCase

import requests
from requests.auth import HTTPBasicAuth


class AuthenticationTest(TestCase):

    def test_token(self):
        url = 'http://localhost:5000/api/v1'
        u = 'ABCD'
        p = 'GLOAT2020'
        res = requests.get(url=f'{url}/users/1')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), {'username': u})
        res = requests.get(f'{url}/token', auth=HTTPBasicAuth(username=u, password=p))
        self.assertEqual(res.status_code, 200)
        token = res.json()['token']
        res = requests.get(f'{url}/resource', auth=HTTPBasicAuth(username=token, password='unused'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), {'data': f'Hello, {u}!'})

    def test_whitelist(self):
        url = 'http://localhost:5000/api/v1'
        u = 'ABCD'
        p = 'GLOAT2020'
        res = requests.get(f'{url}/token', auth=HTTPBasicAuth(username=u, password=p))
        self.assertEqual(res.status_code, 200)
        token = res.json()['token']
        res = requests.post(f'{url}/users/whitelist', auth=HTTPBasicAuth(username=token, password='unused'))
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json(), {'data': f'Hello, {u}, thanks for the whitelist!'})
