import logging
from multiprocessing import Event

from listeners.listener_base import ListenerBase


class UserAuthFileListener(ListenerBase):

    def __init__(self, start_signal_event: Event, daily_frequency: float):
        super().__init__(start_signal_event=start_signal_event, daily_frequency=daily_frequency)

    def listen(self):
        logging.info('listening !!!!')
