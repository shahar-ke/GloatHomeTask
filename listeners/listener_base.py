import datetime
import json
import logging
from abc import ABC, abstractmethod
from multiprocessing import Event
from multiprocessing.context import Process
from time import sleep
from typing import Optional, List

from listeners.listener_state import ListenerState
from server_lib.gloat_server_sdk import GloatServerSDK
from utils.user_info_generator import UserInfoGenerator


class ListenerBase(Process, ABC):

    def __init__(self, start_signal_event: Event, daily_frequency: float = 1):
        super().__init__()
        frequency_sleep_delta_sec = 24 / daily_frequency * 60 * 60
        self.frequency_delta = datetime.timedelta(seconds=frequency_sleep_delta_sec)
        self.start_signal_event: Event = start_signal_event
        logging.info(f'process:{self.start_signal_event}')
        self.state: ListenerState = ListenerState.INIT
        self.error: Optional[Exception] = None
        self.cls_name = self.__class__.__name__

    def run(self):
        try:
            logging.info(f'{self.cls_name} waiting for a signal to start listening')
            self.start_signal_event.wait()
            logging.info(f'{self.cls_name} signal to start listening received')
            self.state = ListenerState.STARTED
            sleep_time_sec = 60
            while True:
                now = datetime.datetime.now()
                wakeup_time = now + self.frequency_delta
                logging.info(f'{self.cls_name}, {self.state=}')
                self.listen()
                logging.info(f'{self.cls_name} done listening, sleeping until {wakeup_time}')
                while self.state != ListenerState.WAKEUP and datetime.datetime.now() < wakeup_time:
                    logging.info(f'{self.cls_name} woke up and going back to sleep')
                    sleep(sleep_time_sec)
                logging.info(f'{self.cls_name} woke up amd going back to listen')
        except Exception as e:
            self.error = e
            self.state = ListenerState.ERROR

    def listen(self):
        users_raw_data = self.fetch_users_data()
        gloat_users_info = self.map_raw_data(users_raw_data=users_raw_data)
        self.send_whitelist(gloat_users_info)

    @abstractmethod
    def fetch_users_data(self) -> List[json]:
        raise NotImplementedError()

    def map_raw_data(self, users_raw_data) -> List[json]:
        mapping = self.get_mapping()
        gloat_users_info = [UserInfoGenerator.generate_from_json(user_data, mapping) for user_data in users_raw_data]
        gloat_users_info = [user_info for user_info in gloat_users_info if user_info is not None]
        return gloat_users_info

    @abstractmethod
    def get_mapping(self):
        raise NotImplementedError()

    def send_whitelist(self, gloat_users_info):
        try:
            gloat_server_sdk = GloatServerSDK(client_id="ABCD", client_secret='password')
            response = gloat_server_sdk.update_white_list(users_info=gloat_users_info)
            if response.code != 201:
                logging.error(f'got {response.code} from server trying to send {gloat_users_info=}')
        except Exception as e:
            logging.exception(e)
            logging.error(f'failed trying to send to server {gloat_users_info}')
