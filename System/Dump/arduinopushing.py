import sys, os, random, time, redis

instance = None

class Pusher(object):

	def initRedis(self, channel):
		self.channel = channel
		self.redisinstance = redis.Redis(host='localhost', port=6379)

	def pushforever(self):
		self.check = True

		while self.check:

			self.value = random.randint(100, 1000)
			self.message = "{ \"nodeId\": \"arduino1\", \"type\": \"Luminosity\", \"value\": " + str(self.value) + " }"

			print 'Pushing to redis on ' + self.channel

			self.redisinstance.publish(self.channel, self.message)

			time.sleep(10)



if __name__ == '__main__':
	sys.path.append(os.path.join(os.path.dirname(__file__), '..\Representation'))
	
	from Objects.params import Params

	instance = Pusher()
	print 'System Gathering created'

	channel = Params.specific_channels["physical.arduino.values"].format("arduino1")

	instance.initRedis(channel)
	print 'Redis connection initialised'

	instance.pushforever()
	print 'Started pushing'


