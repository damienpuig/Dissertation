#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from App import app
from bottle import debug, run, hook, get, CherryPyServer
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
from mongoengine import *



def main():
	socketPort = int(os.environ.get("PORT", 8000))

	register_connection("default", name='dissertation', host='localhost', port=27017)

	run(app, reloader=True, host='127.0.0.1', port=socketPort, server=GeventWebSocketServer)

	bottle.TEMPLATES.clear()

if __name__ == '__main__':
	main()