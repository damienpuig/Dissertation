from bottle import route, run, template, request
import json, redis, gevent
from Services.valueservice import ValueService
from Services.psservice import PsService
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
from Objects.params import Params
from Objects.value import Value
from gevent import monkey
monkey.patch_all()

value_s = ValueService('ValueService')
ps_s = PsService('PsService')


@route('/connect', apply=[websocket])
def receive(ws):
    if request.environ.get('wsgi.websocket'):
        print "test"




        gevent.joinall([
            gevent.spawn(server, ws)
            ])

# def client(ws):
#     while True:
#         print "client started"
#         msg = ws.receive()

#         if msg is not None:
#             if msg is 'STOP':
#                 print "client if stop"
#                 ws.close()
#                 ps_s.punsubscribe()
#             else:
#                 print "client else stop"
#                 ps_s.punsubscribe()
#                 ps_s.psubscribe(msg)

#         gevent.sleep(0)



def server(ws):
        print "server started"
        channel = Params.specific_channels['system.arduinos']
        ps_s.psubscribe(channel)

        while True:
            print "server"
            for output in ps_s.notify():

                if ps_s.isvalidoutput(output):
                    send(ws, output)







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