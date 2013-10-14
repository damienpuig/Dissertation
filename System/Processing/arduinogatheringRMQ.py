import sys
import os
import json
import threading

import redis
import pika
from mongoengine import *


class Listener(threading.Thread):
    def __init__(self, iscomand, lock):
        threading.Thread.__init__(self)
        self.pchannel = Params.specific_channels["system.arduino.values"]
        self.scomandchannel = Params.specific_channels["comands.system"]
        self.queuename = Params.specific_channels["physical.arduinos"]

        self.tLock = lock
        self.iscomand = iscomand


    def initRedis(self, iscomand):

        self.redis = redis.Redis(host='localhost', port=6379)
        self.sredis = redis.Redis(host='localhost', port=6379).pubsub()

        self.comands = {
            'stop': lambda: sys.exit(0),
            'restart': lambda: restart_program()
        }

        if self.iscomand:
            self.sredis.psubscribe(self.scomandchannel)


    def initRabbit(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queuename, durable=True)
        print ' [*] Waiting for messages. To exit press CTRL+C'


    #initialisation of mongoDB if GATHERER LISTENER
    def initMongoDB(self):
        register_connection("default", name='dissertation', host='localhost', port=27017)
        self.device_s = DeviceService('DeviceService')
        self.value_s = ValueService('ValueService')


    # run method will loop on the redis channel.
    # The fun thing here is that the listen() method from the redis-py API is BLOCKING, so we
    # cannot give a callback and we have to wait for a result. Hence, we do not need to declare our own While statement!
    def run(self):

        self.initRedis(self.iscomand)

        if self.iscomand:
            self.checkcomandforever()
        else:
            self.initRabbit()
            self.initMongoDB()
            self.channel.basic_qos(prefetch_count=1)
            self.channel.basic_consume(self.RabbitCallback, queue=self.queuename)
            self.channel.start_consuming()

    def checkcomandforever(self):
        self.sredis.subscribe(Params.specific_channels["comands.system"])

        for message in self.sredis.listen():
            self.processComands(message)

    def RabbitCallback(self, ch, method, properties, body):

        print " [x] Received %r" % (body,)

        #Working with strings and json can be lead to errors. the processing is (try/catch)ed.
        try:

            self.lockprint('ENTRY', str(body))


            #render a json message, easy to work with.
            result = json.loads(body)

            #Details of the message
            ###################################################
            rawDevice = result['device']
            rawValue = result['value']
            ###################################################

            #check if the device exists
            device = self.device_s.getbyname(name=rawDevice['nodeId'])

            #if the device does not exist, we add the device
            if not device.isvalid:
                #details of the new device
                ###################################################
                name = rawDevice['nodeId']
                deviceLocation = [float(rawDevice['location']['longitude']), float(rawDevice['location']['latitude'])]
                ###################################################

                #we add the new device
                device = self.device_s.add(name, 'this is the node ' + name, deviceLocation)

            self.lockprint('DEVICE', device.result.tojson())

            #if the result is valid (from old or new device)
            if device.isvalid:
                #details of the value
                ###################################################
                value = rawValue['value']
                valueType = rawValue['type']
                valueLocation = [float(rawValue['location']['longitude']), float(rawValue['location']['latitude'])]
                completeness = rawValue['qoc']['completeness']
                significance = rawValue['qoc']['significance']
                ###################################################

                #we finally add the value
                newValue = self.value_s.add(device.result, valueType, value, valueLocation, None, completeness,
                                            significance)


                #Once the device/value have been added, we emit using redis publish
                self.emit(device.result.name, newValue)

                print " [x] Done"
                ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception, e:
            self.lockprint('ERROR', e)


    #Emit the entry in database on the system
    def emit(self, devicename, entry):

        channel = self.pchannel.format(devicename)

        #entity converted to json
        payload = entry.tojson()

        self.lockprint('EMIT FROM THREAD {0}, CHANNEL {1}'.format(threading.current_thread(), channel), payload)

        #entity emited
        self.redis.publish(message=payload, channel=channel)


    #If a comand is detected, process the comand
    def processComands(self, data):
        if data['data'] in self.comands:
            self.lockprint('Comand found: ' + data['data'])
            self.comands[data['data']]()


    # shared locked print utility for several listener instance.
    # they have to use the same lock.
    def lockprint(self, prefix, message):
        self.tLock.acquire()

        if prefix:
            print "{0} : {1}".format(prefix, message)
        else:
            print message

        self.tLock.release()


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '..\Representation'))

    from Services.deviceservice import DeviceService
    from Services.valueservice import ValueService
    from Services.servicebase import ServiceBase
    from Objects.params import Params
    from Objects.device import Device
    from Objects.value import Value

    tLock = threading.Lock()

    comandListener = Listener(True, tLock)
    valueListener = Listener(False, tLock)

    comandListener.start()
    valueListener.start()


def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


