import sys
import os
import time
import threading
import random

import redis

# This class simulates the physical network.
# Once the instance create, it pushes values on
class Pusher(threading.Thread):
    def __init__(self, iscomand, arduinos=None):
        threading.Thread.__init__(self)
        if arduinos is None:
            self.arduinos = ["arduino1", "arduino2"]
        else:
            self.arduinos = arduinos

        #Possibility to exit OR restart the program
        self.comands = {
            'stop': lambda: sys.exit(0)
        }

        self.iscomand = iscomand


    #Redis inistialisation, we use the default port.
    def initRedis(self):
        self.redisinstance = redis.Redis(host='localhost', port=6379)

        if self.iscomand:
            self.subscriptionintance = redis.Redis(host='localhost', port=6379).pubsub()

            #If a comand is detected, process the comand

    def processComands(self, data):
        if data['data'] in self.comands:
            self.comands[data['data']]()


    def checkcomandforever(self):
        self.subscriptionintance.subscribe(Params.specific_channels["comands.physical"])

        for message in self.subscriptionintance.listen():
            self.processComands(message)


    def run(self):
        self.initRedis()
        print 'Redis connection initialised for thread '

        if self.iscomand:
            self.checkcomandforever()
        else:
            self.pushforever()


    def pushforever(self):

        #check can be used to shutdown the simulation
        self.check = True

        while self.check:
            #Get ramdom arduinos
            dname = random.choice(self.arduinos)

            #Get a value from its sensors
            raw = random.randint(100, 1000)

            #Defines the quality of context of the value
            quality = "{ \"completeness\": \"1\", \"significance\": \"normal\" }"
            valueLocation = "{\"longitude\": \"40\", \"latitude\": \"30\" }"
            valueContext = "{\"type\": \"Luminosity\", \"value\": " + str(
                raw) + ", \"qoc\": " + quality + ", \"location\": " + valueLocation + "}"

            #Defines the location of the device _ hard coded in that case.
            deviceLocation = "{\"longitude\": \"40\", \"latitude\": \"30\" }"
            deviceContext = "{\"nodeId\": \"" + dname + "\", \"location\": " + deviceLocation + "}"

            # Final message to publish
            message = "{\"device\": " + deviceContext + ", \"value\": " + valueContext + "}"


            # Specific channel for the finall message. The channel is patternised
            channel = Params.specific_channels["physical.arduino.values"].format(dname)

            print 'inserting on ' + channel + ' list, ' + message

            #We push the data on a Redis Key/List.
            self.redisinstance.rpush(channel, message)

            print 'Pushing to redis on ' + channel

            #Publishing on the given channel for notification
            self.redisinstance.publish(channel, Params.global_comands['physical_new_message'])

            time.sleep(10)


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '..\Representation'))

    from Objects.params import Params

    avdevices = ["arduino1", "arduino2", "arduino3", "arduino4"]

    comandListener = Pusher(False, avdevices)
    arduinoPusher = Pusher(True, avdevices)

    comandListener.start()
    arduinoPusher.start()


