#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from App import app
from bottle import debug, run, hook
from mongoengine import *

debug(True)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    print("hello damien from bottle")
    register_connection("default", name='dissertation', host='localhost', port=27017)
    run(app, reloader=True, host='0.0.0.0', port=port)