import sys, os, time, redis, json, datetime, threading, random, pika, atexit

# This class simulates the physical network.
# Once the instance create, it pushes values on
class Pusher(threading.Thread):

	def __init__(self, iscomand, arduinos=None, rabbitHost='localhost', queuename='default'):
		threading.Thread.__init__(self)
		if arduinos is None:
			self.arduinos = ["arduino1", "arduino2"]
		else:
			self.arduinos = arduinos

		#Possibility to exit OR restart the program
		self.comands = {
		'stop': lambda:sys.exit(0),  
		'restart':lambda:restart_program()
		}

		self.iscomand = iscomand
		self.rabbith = rabbitHost
		self.queuename = queuename


	#Redis inistialisation, we use the default port.
	def initRedis(self):
		self.subscriptionintance = redis.Redis(host='localhost', port=6379).pubsub()


	def initRabbit(self, host, queuename):
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue=queuename, durable=True)



	def processComands(self, data):
		if data['data'] in self.comands:
			self.comands[data['data']]()

	def checkcomandforever(self):
		self.subscriptionintance.subscribe(Params.specific_channels["comands.physical"])

		for message in self.subscriptionintance.listen():
			self.processComands(message)


	def run(self):

		if self.iscomand:
			self.initRedis()
			self.checkcomandforever()
		else:
			self.initRabbit(self.rabbith, self.queuename)
			self.pushToRabbitForever()


	def pushToRabbitForever(self):
		while True:

			#Get ramdom arduinos
			dname = random.choice(self.arduinos)

			#Get a value from its sensors
			raw = random.randint(100, 1000)

			#Defines the quality of context of the value
			quality = "{ \"completeness\": \"1\", \"significance\": \"normal\" }"
			valueLocation = "{\"longitude\": \"40\", \"latitude\": \"30\" }"
			valueContext = "{\"type\": \"Luminosity\", \"value\": " + str(raw) + ", \"qoc\": "+ quality +", \"location\": "+ valueLocation +"}"

			#Defines the location of the device _ hard coded in that case.
			deviceLocation = "{\"longitude\": \"40\", \"latitude\": \"30\" }"
			deviceContext = "{\"nodeId\": \""+ dname +"\", \"location\": "+ deviceLocation +"}"

			# Final message to send to queue
			message = "{\"device\": "+ deviceContext +", \"value\": "+ valueContext+"}"

			print 'inserting to RabbitMQ on '+ self.queuename+': '+message

			#send message to Rabbit
			self.channel.basic_publish(exchange='',
                      routing_key=self.queuename,
                      body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))

			time.sleep(5)
	
	@atexit.register
	def onclose():
		if not self.iscomand:
			self.connection.close()




if __name__ == '__main__':
	sys.path.append(os.path.join(os.path.dirname(__file__), '..\Representation'))
	
	from Objects.params import Params

	avdevices = ["arduino1", "arduino2", "arduino3", "arduino4"]

	arduinoPusher = Pusher(False, avdevices, "localhost", Params.specific_channels["physical.arduinos"])
	comandListener = Pusher(True, avdevices, None, None)
	 

	comandListener.start()
	arduinoPusher.start()


