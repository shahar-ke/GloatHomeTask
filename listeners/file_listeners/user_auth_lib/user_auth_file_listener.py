import os
from multiprocessing import Event
from typing import List

from common.type_hints import JSONType
from listeners.file_listeners.user_auth_lib.user_auth_mapping import UserAuthMapping
from listeners.listener_base import ListenerBase


class UserAuthFileListener(ListenerBase):

    UPLOAD_PATH = 'upload'
    FILES_PREFIX = 'auth-users'

    def __init__(self, start_signal_event: Event, daily_frequency: float):
        super().__init__(start_signal_event=start_signal_event, daily_frequency=daily_frequency)
        # this should be persisted to db in production
        self.processed_files = set()

    def fetch_users_data(self) -> List[JSONType]:
        for file_name in os.listdir(self.UPLOAD_PATH):
            if not file_name.startswith(self.FILES_PREFIX):
                continue
            if file_name in self.processed_files:
                continue
            file_path = os.path.join(self.UPLOAD_PATH, file_name)



    def get_mapping(self):
        return UserAuthMapping()
