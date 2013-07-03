from mongoengine import *
from Objects.device import Device
from Services.servicebase import ServiceBase

class DeviceService(ServiceBase):
	def getAllDevices(self, email):
		current = Device.exclude("values").all_fields()
		self.logIt("getAllDevices performed", "")
		return current

	def getDeviceByLocation(self, locationTuple):
		currents = Device.objects(location={"type": "Point", "coordinates": locationTuple}, point__max_distance=1000).exclude("values").limit(1)
		self.logIt("getDeviceByLocation performed", " Found " + len(currents))
		return currents

	def getDeviceByName(self, name):
		current = Device.objects(name=name).exclude("values").first()
		self.logIt("getDeviceByName performed", " Found " + current.name)
		return current

	def getDeviceById(self, id):
		current = Device.objects(id=id).exclude("values").first()
		self.logIt("getDeviceById performed", " Found " + current.name)
		return current

	def addDevice(self, name, description, sensors, location):
		newDevice = Device(name=name, description=description, sensors=sensors, location=location)
		newDevice.save()
		self.logIt("addDevice performed", "description :" + newDevice.description)
		return newDevice

	def removeDevice(self, device):
		device.delete()
		self.logIt("removeDevice performed", current.name + " has been deleted")
		return device

	def removeAllDevices(self):
		Device.drop_collection()
		self.logIt("removeAllDevices performed", " Device collection has been deleted")
		pass

	def updateDevice(self, device):
		device.save()
		self.logIt("updateDevice performed", " Updated on " + device.name)
		pass


	def getValuesByDevice(self, device, limit):
		query = Value.objects.get(device=device)

		if limit is not None:
			query.limit(limit)

		values = query.all()
		return values

	def getValuesByDeviceAndFromDateTime(self, device, limit, date):
		query = Value.objects.filter((Q(device=device) & Q(date__gte=date))
		
		if limit is not None:
			query.limit(limit)

		values = query.all()
		return values

	def addValue(self, ):

