import datetime
import logging
from abc import ABC, abstractmethod
from multiprocessing import Event
from multiprocessing.context import Process
from time import sleep
from typing import Optional

from listeners.listener_state import ListenerState


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

    @abstractmethod
    def listen(self):
        raise NotADirectoryError()
