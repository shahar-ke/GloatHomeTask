import datetime
import logging
from multiprocessing import Event
from typing import List

import requests

from common.type_hints import JSONType
from listeners.client_listeners.acme_lib.acme_mapping import AcmeMapping
from listeners.listener_base import ListenerBase


class AcmeListener(ListenerBase):
    DEFAULT_JSON = [
        {
            "UserId": "A1B2C3",
            "First_name": "Mike",
            "Last_name": "Ross",
            "Email_Id": "mike.r@gloat.com",
            "Manager_userId": 456,
            "Manager_email": "Harvey.S@gloat.com", "Grade level": 8,
            "Department level 1": "Human resources",
            "Department level 2": "SK708",
            "Department level 3": "HR Ops & Delivery",
            "Title": "HR",
            "Division": "Human resources",
            "Location": "Bangalore, India",
            "City": "Bangalore",
            "Country": "IND",
            "Business_unit": "HR Manager",
            "People_Leader": "Y"
        },
        {
            "UserId": "A2B3C4",
            "First_name": "Donna",
            "Last_name": "Paulson",
            "Email_Id": "donna.p@gloat.com",
            "Manager_userId": 456,
            "Manager_email": "Harvey.S@gloat.com",
            "Grade level": 5,
            "Department level 1": "Human resources",
            "Department level 2": "SK708",
            "Department level 3": "HR Ops & Delivery",
            "Title": "HR recruiter",
            "Division": "Human resources",
            "Location": "Bangalore, India",
            "City": "Bangalore",
            "Country": "IND",
            "Business_unit": "HR",
            "People_Leader": "N"
        }
    ]

    def __init__(self, start_signal_event: Event, daily_frequency: int = 1):
        super().__init__(start_signal_event, daily_frequency=daily_frequency)
        self.last_end_date = None
        self.acme_user = 'BBB'
        self.acme_secret = "GLOAT_INTEGRATION"
        self.acme_url = 'https://acme.com/api/v1/authorized-users'

    def process_users_json(self, users_json):
        if not users_json:
            logging.warning('empty users json')
            return

    def fetch_users_data(self) -> List[JSONType]:
        if not self.last_end_date:
            self.last_end_date = datetime.datetime.now() - self.frequency_delta
        from_date = self.last_end_date
        end_date = datetime.datetime.now()
        self.last_end_date = end_date
        params = {'from': str(from_date), 'end': str(end_date)}
        logging.info(f'fetching json from client, from:{self.last_end_date}, end:{end_date}')
        data = {'CLIENT_ID': self.acme_user, 'CLIENT_SECRET': self.acme_secret}
        try:
            response = requests.get(url=self.acme_url, params=params, json=data)
            return response.json()
        except Exception as e:
            logging.exception(e)
            logging.info('returning default json')
            return self.DEFAULT_JSON

    def get_mapping(self):
        return AcmeMapping()
