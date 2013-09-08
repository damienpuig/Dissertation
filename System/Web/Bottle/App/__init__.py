# -*- coding: utf-8 -*-
__version__ = '0.1'
import os
from bottle import Bottle, TEMPLATE_PATH, request, route, hook
from beaker.middleware import SessionMiddleware
import redis

session_opts = {
    'beaker.session.type': 'redis',
	'beaker.session.url': 'localhost:6379',
	'beaker.session.auto': True
}
redis = redis.Redis(host='localhost', port=6379, db=0)
app = SessionMiddleware(Bottle(), session_opts)
TEMPLATE_PATH.insert(0, os.path.join(os.path.dirname(__file__), 'views'))
TEMPLATE_PATH.remove("./views/")

from App.controllers import *