from multiprocessing import Event
from time import sleep

import logging
logging.basicConfig(level=logging.INFO)
from multiprocessing_logging import install_mp_handler
install_mp_handler()
from listeners.file_listeners.user_auth_lib.user_auth_file_listener import UserAuthFileListener


def start_listeners():
    start_signal = Event()
    logging.info(f'main: {start_signal}')
    gloat_file_listener = UserAuthFileListener(start_signal_event=start_signal, daily_frequency=24 * 60 * 60)
    # gloat_json_listener = GloatJsonListener(daily_frequency=1)
    # for listener in [gloat_file_listener, gloat_json_listener]:
    for listener in [gloat_file_listener]:
        listener.start()
        logging.info('sleep 5')
        sleep(2)
        start_signal.set()
        logging.info('sleep 5 done')
    while True:
        logging.info('sleepy')
        sleep(5)


def start_server():
    pass


def main():
    start_listeners()
    start_server()


if __name__ == '__main__':
    main()
