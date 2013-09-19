from mongoengine import *
from Objects.user import User
from Objects.result import Result
from Services.servicebase import ServiceBase
from bson.objectid import ObjectId

#User service
#
#Basic implementation of a service executing queries
#to the mongoDB database.
#Most of the queries are encapsulation in a Result instance.
#Every query is logged through ServiceBase.
class UserService(ServiceBase):

	def __init__(self, instancename):
		ServiceBase.__init__(self, instancename)

	def getbyemail(self, email):
		query = lambda x:User.objects(email=x).first()
		result = Result().safe_execute(query,email)

		if result.isvalid:
			self.logit("getbyemail performed", result.result.tojson())
		else:
			self.logit("getbyemail performed with error", result.error)
		return result

	def getbyid(self, id):
		query = lambda x:User.objects(id=ObjectId(x)).first()
		result = Result().safe_execute(query, id)

		if result.isvalid:
			self.logit("getbyid performed", result.result.tojson())
		else:
			self.logit("getbyid performed with error", result.error)
		return result

	def add(self, email):
		newUser = User(email=email)
		newUser.save()
		self.logit("add performed", "{0} has been added".format(newUser.tojson()))
		return newUser

	def delete(self, id):
		result = getbyid(id)

		if result.isvalid:
			result.result.delete()
			self.logit("delete performed", result.result.tojson() + " has been deleted")
		else:
			self.logit("delete performed with error", result.error)
		

	def deleteall(self):
		User.drop_collection()
		self.logit("deleteall performed", "User collection has been deleted")
		