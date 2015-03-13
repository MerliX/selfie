# -*- coding: utf-8 -*-

PHOTO_PATH = '/opt/selfie-dump/selfies/'

SQLITE_DB_PATH = '/opt/selfie-dump/base.db'
POSTGRES_DB_NAME = 'selfie'
POSTGRES_USER = 'selfie'
POSTGRES_HOST = 'db.selfie-dump.ru'
USE_POSTGRES = True

SERVER = 'gunicorn'

HOST = 'localhost'
PORT = 8080
DEBUG = True

SELFIE_REWARD = 10


try:
    from local_settings import *
except ImportError:
    pass
