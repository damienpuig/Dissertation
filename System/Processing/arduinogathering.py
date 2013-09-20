import sys, os, time, redis, json, datetime, threading
from rlock import Rlock
from mongoengine import *

class Listener(threading.Thread):

	#GENERAL INFORMATION: If the iscomand is true, the listener will have a totally different behaviour.
	#EACH INSTANCE OF LISTENER IS A THREAD.
	#
	#COMAND LISTENER (iscomand = True)
	#The listener will subscribe to the comands.system channel and wait for comands
	#
	#GATHERER LISTENER (iscomand = False)
	#The listener will subscribe to the system.arduino.values (which is a Redis pattern for pubsub accepting every arduino)
	#and waits for new entries
	#
	#Since the program will use two instances, we can shutdown it using a single instance of listener, which is the COMAND LISTENER
	def __init__(self, iscomand, tLock):
              threading.Thread.__init__(self)
              self.initRedis(iscomand)
              self.initMongoDB(iscomand)
              self.tLock = tLock
              self.pchannel = Params.specific_channels["system.arduino.values"]

    # We init Redis depending on the Listener Behaviour
	def initRedis(self, iscomand):

		self.redis = redis.Redis(host='localhost', port=6379)
		self.sredis = redis.Redis(host='localhost', port=6379).pubsub()
		self.rLock = Rlock(self.redis)

		#Possibility to exit OR restart the program
		self.comands = {
		'stop': lambda:sys.exit(0),  
		'restart':lambda:restart_program()
		}

		self.iscomand = iscomand

		#Subscriptions
		if self.iscomand:
			self.schannel = Params.specific_channels["comands.system"]
			self.sredis.psubscribe(self.schannel)
		else:
			self.schannel = Params.specific_channels["physical.arduinos"]
			self.sredis.psubscribe(self.schannel)


	#initialisation of mongoDB if GATHERER LISTENER
	def initMongoDB(self, iscomand):
		if not self.iscomand:
			register_connection("default", name='dissertation', host='localhost', port=27017)
			self.device_s = DeviceService('DeviceService')
			self.value_s = ValueService('ValueService')

	# run method will loop on the redis channel.
	# The fun thing here is that the listen() method from the redis-py API is BLOCKING, so we
	# cannot give a callback and we have to wait for a result. Hence, we do not need to declare our own While statement!
	def run(self):
		print 'Started Redis on ' + self.schannel
		for message in self.sredis.listen():
			self.lockprint('NEW MESSAGE', message)

			if self.iscomand:
				self.processComands(message)
			else:
				self.processEntry(message)


	# If a message is found, we process it.
	def processEntry(self, data):

		#If the message does not contains any data, return.
		if not ('data' in data):
			return

		#Working with strings and json can be lead to errors. the processing is (try/catch)ed.
		try:


			self.lockprint('LOOKING FOR LIST ', data['channel'])

			self.rLock.acquire()

			#get the entry associated with the subscription
			entry = self.redis.lpop(data['channel'])


			self.rLock.release()


			self.lockprint('ENTRY', str(entry))

			#render a json message, easy to work with.
			result = json.loads(entry)


			#Details of the messages
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
				valueLocation =  [float(rawValue['location']['longitude']), float(rawValue['location']['latitude'])]
				completeness = rawValue['qoc']['completeness']
				significance = rawValue['qoc']['significance']
				###################################################

				#we add finally add the value
				newValue = self.value_s.add(device.result, valueType, value, valueLocation, None, completeness, significance)


				#Once the device/value have been added, we emit using redis publish
				self.emit(device.result.name, newValue)

		except Exception, e:
			self.lockprint('ERROR', e)

	#If a comand is detected, process the comand
	def processComands(self, data):
		if data['data'] in self.comands:
			self.lockprint('Comand found: ' + data['data'])
			self.comands[data['data']]()

	#Emit the entry in database on the system
	def emit(self, devicename, entry):

		channel = self.pchannel.format(devicename)

		#entity converted to json
		payload = entry.tojson()

		self.lockprint('EMIT FROM THREAD {0}, CHANNEL {1}'.format(threading.current_thread(), channel), payload)

		#entity emited
		self.redis.publish(message=payload, channel=channel)

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
    os.execl(python, python, * sys.argv)


