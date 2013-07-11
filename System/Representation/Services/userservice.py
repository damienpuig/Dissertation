from mongoengine import *
from Objects.user import User
from Services.servicebase import ServiceBase, Result

class UserService(ServiceBase):

	def __init__(self, instancename):
		ServiceBase.__init__(self, instancename)

	def getbyemail(self, email):
		query = lambda x:User.objects(email=x).first()
		result = Result().safe_execute(query,email)

		if result.isvalid:
			self.logit("getbyemail performed", result.result.email)
		else:
			self.logit("getbyemail performed", "user not found")
		return result

	def getbyid(self, id):
		query = lambda x:User.objects(_id=x).first()
		result = Result().safe_execute(query, id)

		if result.isvalid:
			self.logit("getbyid performed", result.result.email)
		else:
			self.logit("getbyid performed", "user not found")
		return result

	def add(self, email):
		newuser = User(email=email)
		newuser.save()
		self.logit("add performed", newuser.email)
		return newuser

	def delete(self, id):
		result = getUserById(id)

		if result.isvalid:
			result.result.delete()
			self.logit("delete performed", result.result.email + " has been deleted")
		else:
			self.logit("delete performed", "user not found for deletion")
		

	def deleteall(self):
		User.drop_collection()
		self.logit("deleteall performed", " User collection has been deleted")
		