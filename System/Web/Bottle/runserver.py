#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import bottle
from bottle import run, CherryPyServer
from mongoengine import *

from App import app



#Entry point to start a web server using bottle
#The server is a cherryPy server.
def main():
    webPort = int(os.environ.get("PORT", 8080))

    register_connection("default", name='dissertation', host='localhost', port=27017)

    run(app, reloader=True, host='127.0.0.1', port=webPort, server=CherryPyServer)

    bottle.TEMPLATES.clear()


if __name__ == '__main__':
    main()