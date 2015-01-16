# -*- coding: utf-8 -*-

PHOTO_PATH = '/opt/selfie/selfies/'
DB_PATH = '/opt/selfie/base.db'
HOST = 'localhost'
PORT = 8080
DEBUG = False


try:
	from local_settings import *
except ImportError:
	pass