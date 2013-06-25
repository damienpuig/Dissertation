# -*- coding: utf-8 -*-
__version__ = '0.1'
from bottle import Bottle, TEMPLATE_PATH
app = Bottle()
TEMPLATE_PATH.append("./App/views/")
TEMPLATE_PATH.remove("./views/")
from App.controllers import *
