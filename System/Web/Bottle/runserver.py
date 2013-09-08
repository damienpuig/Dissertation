#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from App import app
from bottle import debug, run, hook, get
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
from mongoengine import *



def main():
	port = int(os.environ.get("PORT", 8080))
	print("hello damien from bottle")
	register_connection("default", name='dissertation', host='localhost', port=27017)
	run(app, reloader=True, host='127.0.0.1', port=port, server=GeventWebSocketServer)
	bottle.TEMPLATES.clear()

if __name__ == '__main__':
	main()