from mongoengine import *
from Objects.device import Device
from Objects.value import Value
from Services.servicebase import ServiceBase

#Coment service
#
#Permit to add a single element, or several elements
#Most of the queries are logged through ServiceBase.
class CommentService(ServiceBase):

	def __init__(self, instancename):
		ServiceBase.__init__(self, instancename)

	def add(self, value, comment):
		value.update(add_to_set__comments=[comment])
		return value

	def adds(self, value, comments):
		value.update(add_to_set__comments=comments)
		return value