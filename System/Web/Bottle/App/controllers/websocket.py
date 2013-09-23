from bottle import route, run, template, request
import json, redis, gevent
from Services.valueservice import ValueService
from Services.psservice import PsService
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
from Objects.params import Params
from Objects.value import Value
from gevent import monkey

#patch the threading behaviour to switch 
#for a thread into another thread.
monkey.patch_all()

#Service Declaration
###########################################
value_s = ValueService('ValueService')
ps_s = PsService('PsService')
###########################################


#ROUTE /connect
#Socket connection to redis pubsub
@route('/connect', apply=[websocket])
def receive(ws):
    if request.environ.get('wsgi.websocket'):

        #Switch from a thread into another thread
        # to check socket entries.
        # 
        # Infortunately, this does not work because
        # redis implementation is BLOCKING on
        # the listen method (No callback implementation on Redis-py?).
        gevent.joinall([
            gevent.spawn(client, ws),
            gevent.spawn(server, ws)
            ])

def client(ws):
    while True:
        print "client started"
        msg = ws.receive()

        if msg is not None:
            if msg is 'STOP':
                print "client if stop"
                ws.close()
                ps_s.punsubscribe()
            else:
                print "client else stop"
                ps_s.punsubscribe()
                ps_s.psubscribe(msg)

        gevent.sleep(0)


#server delivering, through socket, message coming from
#redis subscription. 
def server(ws):
        print "server started"
        channel = Params.specific_channels['system.arduinos']
        ps_s.psubscribe(channel)

        while True:
            #The notify methos is the listen BLOCKING method.
            for output in ps_s.sredis.listen():

                if ps_s.isvalidoutput(output):
                    send(ws, output)


#Since each data are processed using redis subscription pubsub
#we compute the message and send back to the client.
#Data are also HTML computed on the fly using bottle template.
def send(ws, output):
    raw = json.loads(output['data'])
    value = value_s.getbyid(raw['id'])

    if not value.isvalid:
        result = {
        "count": 0
        }
    else:
        result = {
        "data" : template('template/value', value=value.result),
        "count": 1
        }

    ws.send(json.dumps(result))