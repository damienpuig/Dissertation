
class Params:
	global_channels = {
	#all physical events
	"physical": "physical.*",
	#all system event ( logs or error )
	"system": "system.*",
	#all comands
	"comands": "comands.*"
	}

	#List of the channels used in the application
	#Some channels finish by a *, meaning that that are patterns for redis-pubsub
	#Some channels finish have {0}, meaning that they have to be 
	#completed by a string, namely the name of the arduino
	specific_channels = {

	#raw data from all devices of the physical network
	"physical.arduinos": "physical.arduinos.*",

	#raw data from specific device of the physical network
	"physical.arduino": "physical.arduinos.{0}",

	#raw values from specific device of the physical network
	"physical.arduino.values": "physical.arduinos.{0}.values",

	#data from all devices of the system
	"system.arduinos": "system.arduinos.*",

	#data from specific device of the system
	"system.arduino": "system.arduinos.{0}",

	#values from specific device of the system
	"system.arduino.values": "system.arduinos.{0}.values",

	"system.log": "system.logs",
	"system.errors": "system.errors",

	#commands that act on the physical environment
	"comands.physical":"comands.physical",
	
	#comands that act on the system itself
	"comands.system":"comands.system"
	}