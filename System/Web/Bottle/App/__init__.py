# -*- coding: utf-8 -*-
__version__ = '0.1'
from bottle import Bottle, TEMPLATE_PATH, request, route, hook
from beaker.middleware import SessionMiddleware

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}
app = SessionMiddleware(Bottle(), session_opts)
TEMPLATE_PATH.append("./App/views/")
TEMPLATE_PATH.remove("./views/")

from App.controllers import *