import sys, os, time, redis, json, datetime, threading
from mongoengine import *


class Listener(threading.Thread):

	def __init__(self, iscomand, lock):
              threading.Thread.__init__(self)
              self.initRedis(iscomand)
              self.initMongoDB()
              self.lock = lock
              self.pchannel = Params.specific_channels["system.arduino.values"]

	def initRedis(self, iscomand):

		self.predis = redis.Redis(host='localhost', port=6379)
		self.sredis = redis.Redis(host='localhost', port=6379).pubsub()

		self.comands = {
		'stop': lambda:sys.exit(0),  
		'restart':lambda:restart_program()
		}

		self.iscomand = iscomand

		if self.iscomand:
			self.schannel = Params.specific_channels["comands.system"]
			self.sredis.psubscribe(self.schannel)
		else:
			self.schannel = Params.specific_channels["physical.arduinos"]
			self.sredis.psubscribe(self.schannel)



	def initMongoDB(self):
		register_connection("default", name='dissertation', host='localhost', port=27017)
		self.device_s = DeviceService('DeviceService')
		self.value_s = ValueService('ValueService')

	def run(self):

		while True:
			print 'Checking Redis on ' + self.schannel
			#datarcvd = 0
			for message in self.sredis.listen():
				self.lockprint('NEW MESSAGE', message)
				# datarcvd += 1
				# if datarcvd == 10:
				# 	print 'PUBLISHING STOP'
				# 	self.redisinstance.publish(self.channel2, 'stop')
				# print 'Receiving..'
				if self.iscomand:
					self.processComands(message)
				else:
					self.processEntry(message)


			time.sleep(1)



	def processEntry(self, data):

		if not ('data' in data):
			return

		try:
			entry = data['data']
			self.lockprint('ENTRY', str(entry))

			result = json.loads(entry)
			namedevice = result['nodeId']

			device = self.device_s.getbyname(name=namedevice)

			if not device.isvalid:
				device = self.device_s.add(namedevice, 'this is the node ' + namedevice, [40, 30])

			self.lockprint('DEVICE', str(device.result))

			if device.isvalid:
				newValue = self.value_s.add(device.result, result['type'], result['value'], None)

				self.emit(device.result.name, newValue)

		except Exception, e:
			self.lockprint('ERROR', e)

	def processComands(self, data):
		if data['data'] in self.comands:
			self.lockprint('Comand found: ' + data['data'])
			self.comands[data['data']]()

	def emit(self, devicename, entry):

		channel = self.pchannel.format(devicename)
		payload = entry.tojson()

		self.lockprint('EMIT FROM THREAD {0}, CHANNEL {1}'.format(threading.current_thread(), channel), payload)
		self.predis.publish(message=payload, channel=channel)

	def lockprint(self, prefix, message):
		self.lock.acquire()

		if prefix:
			print "{0} : {1}".format(prefix, message)
		else:
			print message

		self.lock.release()






if __name__ == '__main__':
	sys.path.append(os.path.join(os.path.dirname(__file__), '..\Representation'))
	
	from Services.deviceservice import DeviceService
	from Services.valueservice import ValueService
	from Services.servicebase import ServiceBase
	from Objects.params import Params
	from Objects.device import Device
	from Objects.value import Value

	lock = threading.Lock()

	comandListener = Listener(True, lock)
	#comandListener.setDaemon(True)
		
	valueListener = Listener(False, lock)
	#valueListener.setDaemon(True)

	comandListener.start()
	valueListener.start()

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)


