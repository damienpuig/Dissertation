from mongoengine import *
from Objects.device import Device
from Objects.value import Value
from Services.servicebase import ServiceBase

class ValueService(ServiceBase):

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

	def createOrUpdateValue(self, value):
		value.save()
		return value

	def deleteValue(self, value):
		value.delete()
		return value

	def deleteAllValueFromDevice(self, device):
		device.values = None
		device.save()
		return device