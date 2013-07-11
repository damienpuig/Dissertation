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

		result = Result().safe_execute(query, device, limit)
		return result

	def getbydeviceandtime(self, device, limit, date):
		def query(d, date, l):
			builder = Value.objects.filter((Q(device=d) & Q(date__gte=date)))
			if not (limit is None):
				builder.limit(l)
			return builder.all()

		result = Result().safe_execute(query, device, date, limit)
		return result

	def addvalue(self, device, valuetype, value, comment):
		newvalue = Value(valueType=valuetype, value=value)

		if not (comment is None):
			newvalue.comments = [comment]

		newvalue.save()
		device.update(add_to_set__values=[newvalue])
		return device

	


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
