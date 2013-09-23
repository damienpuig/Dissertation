import redis

#creation of the event manager connection
self.redisPublisher = redis.Redis(host='localhost', port=6379)

# Creation of the message to send
message = "this information is coming from arduino1 node"

#send the message on the given channel called "physical.arduinos.arduino1"
self.redisPublisher.publish("physical.arduinos.arduino1", message)




#creation of the event manager connection for subscription
self.redisSubscriber = redis.Redis(host='localhost', port=6379).pubsub()

#psubscribe (PATTERN SUBSCRIBE) to given channel "physical.arduinos.*"
self.redisSubscriber.psubscribe("physical.arduinos.*")

#define a callback if a message is received
def callback(message):
	print message

#give the callback to a asynchronous listener.
self.redisSubscriber.asyncListen(callback)



from contentbus import Bus

class Arduino(object):
    def __init__(self, name, val):
        self.name = name
        self.value = val
        
    def __str__(self):
        return "Arduino(%s, %s)" % (self.name, self.val)

def print_message_for(name):
    def print_message(msg):
        print("%s received message: sender=%s object=%s" % (name, msg.sender, msg.object))

    return print_message

#We declare a content-based Publish/Subscribe Bus.
psService = Bus(client='psService')


#We subscribe to two channel instances
#
#The first subscription will get every entities that have name="arduino1"
#the second subscription will get every intities that have a value between 450 and 750
psService.subscribe(print_message_for('psService'), Arduino, name="arduino1")
psService.subscribe(print_message_for('psService'), Arduino, value__in_range =(450, 750))


#We publish information
psService.send(Arduino("arduino1", 600)) #1
psService.send(Arduino("arduino1", 800)) #2
psService.send(Arduino("arduino1", 100)) #3
psService.send(Arduino("arduino1", 500)) #4

psService.send(Arduino("arduino2", 300)) #5
psService.send(Arduino("arduino2", 550)) #6


#Here the result:
#
#First subscription gets 1, 2, 3, 4
#Second subscription gets 1, 4, 6
