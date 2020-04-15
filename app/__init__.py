# coding: utf-8

import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_assets import Environment, Bundle
from flask_session import Session

from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
assets = Environment(app)
socketio = SocketIO(app, 
                    manage_session=False)
Session(app)


# Set up logging
file_handler = RotatingFileHandler('logs/ringingroom.log','a', 1 * 1024 * 1024, 10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
app.logger.setLevel(logging.INFO)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.info('Ringing Room startup')

def log(message):
    app.logger.info(message)


# asset bundles
bundles = {

    'js_landing':   Bundle( 'landing.js',
                            filters='jsmin', 
                            output='gen/landing.%(version)s.js'),

    'js_rr':        Bundle('ringing_room.js',
                           'audio.js',
                           # filters='jsmin',
                            output='gen/rr.%(version)s.js'),

    'css_static':   Bundle( 'css/static.css',
                            output='gen/static.%(version)s.css'),

    'css_rr':   Bundle( 'css/ringing_room.css',
                            output='gen/rr.%(version)s.css'),
}

assets.register(bundles)

from app.models import *

# make the tower dict
towers = TowerDict()

from app import routes, models, listeners
