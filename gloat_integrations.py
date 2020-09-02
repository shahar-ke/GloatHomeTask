#!/usr/bin/env python
import logging
from multiprocessing import Event
from time import sleep

from flask import Flask

from listeners.client_listeners.acme_lib.acme_listener import AcmeListener
from listeners.file_listeners.user_auth_lib.user_auth_file_listener import UserAuthFileListener
from server_lib.blueprints.app_users import app_users
from server_lib.models.database import db
from server_lib.models.user_model import User


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app


def setup_database(app):
    with app.app_context():
        db.init_app(app)
        db.drop_all()
        db.create_all()
        user = User()
        user.username = "ABCD"
        user.hash_password("GLOAT2020")
        db.session.add(user)
        db.session.commit()
        for raw in User.query.all():
            print(raw)


def start_listeners():
    start_signal = Event()
    logging.info(f'main: {start_signal}')
    gloat_file_listener = UserAuthFileListener(start_signal_event=start_signal, daily_frequency=24 * 60 * 60)
    gloat_json_listener = AcmeListener(start_signal_event=start_signal, daily_frequency=1)
    for listener in [gloat_file_listener, gloat_json_listener]:
        listener.start()
        logging.info('sleep 5')
        sleep(2)
        start_signal.set()
        logging.info('sleep 5 done')
    while True:
        logging.info('sleepy')
        sleep(5)


def main():
    app = create_app()
    setup_database(app)
    app.register_blueprint(app_users)
    # start_listeners()
    app.run(debug=True)


if __name__ == '__main__':
    main()
