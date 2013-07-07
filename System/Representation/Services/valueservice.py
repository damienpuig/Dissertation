from mongoengine import *
from Objects.device import Device
from Objects.value import Value
from Services.servicebase import ServiceBase, Result

class ValueService(ServiceBase):

	def __init__(self, instancename):
		ServiceBase.__init__(self, instancename)

	def getbydevice(self, device, limit):
		def query(d, l):
			builder = Value.objects.get(device=d)
			if not (limit is None):
				builder.limit(l)
			return builder.all()

		current = Result().safe_execute(query, device, limit)
		return current

	def getbydeviceandtime(self, device, limit, date):
		query = Value.objects.filter((Q(device=device) & Q(date__gte=date)))
		
		if not (limit is None):
			query.limit(limit)

		values = query.all()
		return values

	def createorupdate(self, value):
		value.save()
		return value

	def delete(self, value):
		value.delete()
		return value

	def deleteallbydevice(self, device):
		device.values = None
		device.save()
		return device

	def deleteall(self):
		Value.drop_collection()
		self.logIt("deleteall performed", " Value collection has been deleted")
