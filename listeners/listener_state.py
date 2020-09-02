from enum import Enum


class ListenerState(Enum):
    INIT = 'init'
    STARTED = 'started'
    DONE = 'done'
    ERROR = 'error'
    WAKEUP = 'wakeup'
