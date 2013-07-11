from mongoengine import *
from Objects.device import Device
from Objects.value import Value
from Services.servicebase import ServiceBase

class DeviceService(ServiceBase):

	def __init__(self, instancename):
		ServiceBase.__init__(self, instancename)

	def getall(self):
		current = Device.exclude("values").all_fields()
		self.logit("getAllDevices performed", "")
		return current

	def getbylocation(self, locationTuple):
		currents = Device.objects(location={"type": "Point", "coordinates": locationTuple}, point__max_distance=1000).exclude("values").limit(1)
		self.logit("getDeviceByLocation performed", " Found " + len(currents))
		return currents

	def getbyname(self, name):
		current = Device.objects(name=name).exclude("values").first()
		#self.logit("getDeviceByName performed", " Found " + current.name)
		return current

	def getbyid(self, id):
		current = Device.objects(id=id).exclude("values").first()
		self.logit("getDeviceById performed", " Found " + current.name)
		return current

	def add(self, name, description, location):
		newDevice = Device(name=name, description=description, location=location)
		newDevice.save()

		self.logit("addDevice performed", "description :" + newDevice.description)
		return newDevice

	def delete(self, device):
		device.delete()
		self.logit("removeDevice performed", current.name + " has been deleted")
		return device

	def deleteall(self):
		Device.drop_collection()
		self.logit("removeAllDevices performed", " Device collection has been deleted")
		

	def update(self, device):
		device.save()
		self.logit("updateDevice performed", " Updated on " + device.name)