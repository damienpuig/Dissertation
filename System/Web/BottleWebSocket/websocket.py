from bottle import get, run, template
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
import time

@get('/')
def index():
    return template('index')

@get('/websocket', apply=[websocket])
def echo(ws):
    while True:
        time.sleep(5)
        send(ws)

def send(ws):
	ws.send("socket ready to push data to client")	

run(host='127.0.0.1', port=8000, server=GeventWebSocketServer)