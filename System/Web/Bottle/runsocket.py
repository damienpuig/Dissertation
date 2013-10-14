#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import bottle
from bottle import run
from mongoengine import *

from bottle.ext.websocket import GeventWebSocketServer, websocket



#Entry point to start a socket server using bottle
def main():
    socketPort = int(os.environ.get("PORT", 8000))

    register_connection("default", name='dissertation', host='localhost', port=27017)

    run(host='127.0.0.1', port=socketPort, server=GeventWebSocketServer)

    bottle.TEMPLATES.clear()


if __name__ == '__main__':
    main()