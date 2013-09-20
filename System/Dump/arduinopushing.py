import sys, os, time, redis, random

# This class simulates the physical network.
# Once the instance create, it pushes values on
class Pusher(object):

	def __init__(self, arduinos=None):
		if arduinos is None:
			self.arduinos = ["arduino1", "arduino2"]
		else:
			self.arduinos = arduinos


	#Redis inistialisation, we use the default port.
	def initRedis(self):
		self.redisinstance = redis.Redis(host='localhost', port=6379)


	def pushforever(self):

		#check can be used to shutdown the simulation
		self.check = True

		while self.check:

			#Get ramdom arduino
			dname = random.choice(self.arduinos)

			#Get a value from its sensor
			raw = random.randint(100, 1000)

			#Defines the quality of context of the value
			quality = "{ \"completeness\": \"1\", \"significance\": \"normal\" }"
			valueLocation = "{\"longitude\": \"40\", \"latitude\": \"30\" }"
			valueContext = "{\"type\": \"Luminosity\", \"value\": " + str(raw) + ", \"qoc\": "+ quality +", \"location\": "+ valueLocation +"}"

			#Defines the location of the device
			deviceLocation = "{\"longitude\": \"40\", \"latitude\": \"30\" }"
			deviceContext = "{\"nodeId\": \""+ dname +"\", \"location\": "+ deviceLocation +"}"

			# Final message to publish
			message = "{\"device\": "+ deviceContext +", \"value\": "+ valueContext+"}"


			# Specific channel for the finall message. The channel is patternised
			channel = Params.specific_channels["physical.arduino.values"].format(dname)



			print 'inserting on '+ channel+' list, '+message

			self.redisinstance.rpush(channel, message)


			print 'Pushing to redis on ' + channel

			#Publishing on the given channel
			self.redisinstance.publish(channel,  Params.global_comands['physical_new_message'])

			time.sleep(10)



if __name__ == '__main__':
	sys.path.append(os.path.join(os.path.dirname(__file__), '..\Representation'))
	
	from Objects.params import Params

	#Set 4 arduinos
	instance = Pusher(["arduino1", "arduino2", "arduino3", "arduino4"])
	print 'System Gathering created'


	instance.initRedis()
	print 'Redis connection initialised'

	instance.pushforever()
	print 'Started pushing'


