import redis

from Services.servicebase import ServiceBase



#Pub Sub service
#
#Basic implementation of a service executing publish/subscription
#on a given channel.
#psubscribe uses content-based patterns.
#Most of the queries are logged through ServiceBase.
class PsService(ServiceBase):
    def __init__(self, instancename):
        ServiceBase.__init__(self, instancename)
        self.sredis = redis.Redis(host='localhost', port=6379).pubsub()
        self.predis = redis.Redis(host='localhost', port=6379)
        self.schannel = None
        self.pchannel = None
        self.commands = {}


    def subscribe(self, channel):
        self.schannel = channel
        self.sredis.subscribe(self.schannel)

    def psubscribe(self, channel):
        self.schannel = channel
        self.sredis.psubscribe(self.schannel)

    def unsubscribe(self):
        self.schannel = []
        self.sredis.unsubscribe(self.schannel)

    def punsubscribe(self):
        self.schannel = []
        self.sredis.punsubscribe(self.schannel)

    def notify(self, channel, payload):
        self.pchannel = channel
        self.predis.publish(self.pchannel, payload)

    def isvalidchannel(self, message):
        if not ('channel' in message):
            return False

        if not self.schannel is message['channel']:
            return False

        if self.scomands is message.channel:
            if message['data'] in self.commands:
                self.logit('Comand found', message['data'])
                self.commands[message['data']]()
                return True

        if message.channel in Params.specific_channels:
            self.logit('Change subscription', message.channel)
            self.sredis.punsubscribe()
            self.sredis.psubscribe(message.channel)
            return True

        return False

    def isvalidoutput(self, entry):
        if not (('data' in entry) and (entry['pattern'] is not None)):
            return False
        return True