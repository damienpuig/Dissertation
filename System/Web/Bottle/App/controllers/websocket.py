from bottle import get, run, template
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
import time

@get('/connect', apply=[websocket])
def connect(ws):
    while True:
        time.sleep(5)
        send(ws)

def send(ws):
	ws.send("socket ready to push data to client")