import sys, os, random
import time
import redis

instance = None

class Pusher(object):

	def initRedis(self):
		self.channel = 'sensors.arduino1'
		self.redisinstance = redis.Redis(host='localhost', port=6379)

	def pushforever(self):
		self.check = True

		while self.check:

			self.value = random.randint(100, 1000)
			self.message = "{ \"nodeId\": arduino1, \"type\": \"Luminosity\", \"value\": " + str(self.value) + " }"

			print 'Pushing to redis on ' + self.channel

			self.redisinstance.publish(self.channel, self.message)

			time.sleep(5)



if __name__ == '__main__':
	instance = Pusher()
	print 'System Gathering created'

	instance.initRedis()
	print 'Redis connection initialised'

	instance.pushforever()
	print 'Started pushing'


