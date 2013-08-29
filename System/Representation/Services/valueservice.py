from mongoengine import *
from Objects.device import Device
from Objects.value import Value
from Objects.result import Result
from Services.servicebase import ServiceBase

class ValueService(ServiceBase):

	def __init__(self, instancename):
		ServiceBase.__init__(self, instancename)

	def getbydevice(self, device, limit):
		query = lambda i:Device.objects.get(id=i)

		result = Result().safe_execute(query, device.id)

		if result.isvalid:
			if not (limit is None) and result.result.values:
				result = result.result.values[:limit]
			self.logit("getbydevice performed", "{0} entries found".format(len(result.result.values)))
		else:
			self.logit("getbydevice performed with error", result.error)
		return result

	def getbytime(self, limit, date):
		def query(date, l):
			builder = Value.objects.filter(Q(date__gte=date))
			if not (limit is None):
				builder.limit(l)
			return builder.all()

		result = Result().safe_execute(query, date, limit)

		if result.isvalid:
			self.logit("getbytime performed", "{0} entries found".format(len(result.result.values)))
		else:
			self.logit("getbytime performed with error", result.error)
		return result

	def add(self, device, valuetype, value, comment):
		newValue = Value(valueType=valuetype, value=value)

		if not (comment is None):
			newValue.comments = [comment]

		newValue.save()

		self.logit("add performed", "{0} has been added".format(str(newValue)))

		device.update(add_to_set__values=[newValue])

		self.logit("update performed", "{0} has been updated".format(str(device)))

		return device

	def delete(self, value):
		value.delete()
		self.logit("delete performed", str(value) + " has been deleted")
		return value

	def deleteallbydevice(self, device):
		lenght = len(device.values)
		device.values = None
		device.save()
		self.logit("deleteallbydevice performed", "device: {0}, entries:{1}".format(str(device), lenght))
		return device

	def deleteall(self):
		Value.drop_collection()
		self.logIt("deleteall performed", "Value collection has been deleted")
