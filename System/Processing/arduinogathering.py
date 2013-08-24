import sys, os
import time
import redis
import json
from mongoengine import *

synchonisation = 2
instance = None

class Listener(object):

	def initRedis(self):
		self.channel = 'sensors.arduino1'
		self.channel2 = 'system.arduinogathering.command'
		self.redisinstance = redis.Redis(host='localhost', port=6379)
		self.redisps = self.redisinstance.pubsub()
		self.redisps.subscribe(self.channel)
		self.redisps.subscribe(self.channel2)
		self.commands = {'stop': lambda:sys.exit(0), 
		'continue': lambda:sys.exit(0), 'restart':lambda:sys.exit(0)}


	def initMongoDB(self):
		register_connection("default", name='dissertation', host='localhost', port=27017)
		self.log_s = ServiceBase('ServiceBase')
		self.device_s = DeviceService('DeviceService')
		self.value_s = ValueService('ValueService')



	def listen(self):
		while True:
			print 'Checking Redis on ' + self.channel
			#datarcvd = 0
			for message in self.redisps.listen():
				print message
				# datarcvd += 1
				# if datarcvd == 10:
				# 	print 'PUBLISHING STOP'
				# 	self.redisinstance.publish(self.channel2, 'stop')
				# print 'Receiving..'
				
				if self.checkchannels(message):
					self.processentry(message['data'])


			time.sleep(1)

	def checkchannels(self, data):
		currentchannel = data['channel']
		print('checking on ' + currentchannel)

		if currentchannel == self.channel:
			return True

		elif currentchannel == self.channel2:
			if data['data'] in self.commands:
				print('Command found: ' + data['data'])
				self.commands[data['data']]()
				return False
		else:
			return False




	def processentry(self, entry):

		print('Entry found: ' + entry.__str__())
		try:
			result = json.loads(entry)
			namedevice = result['nodeId']

			device = self.device_s.getbyname(name=namedevice)

			print type(device)

			if device is None:
				print 'New device'
				device = self.device_s.add(result['nodeId'].__str__(), 'this is the node number ' + namedevice, [40, 30])

			self.value_s.add(device, result['type'], result['value'], None)

		except Exception, e:
			print e



if __name__ == '__main__':
	sys.path.append(os.path.realpath('d:\GitHub\Dissertation\System\Representation'))
	print sys.path
	from Services.deviceservice import DeviceService
	from Services.valueservice import ValueService
	from Services.servicebase import ServiceBase
	from Objects.device import Device
	from Objects.value import Value

	instance = Listener()
	print 'Listener created'

	instance.initRedis()
	print 'Redis connection initialised'

	instance.initMongoDB()
	print 'MongoDB connection initialised'

	instance.listen()
	print 'Started listening'


