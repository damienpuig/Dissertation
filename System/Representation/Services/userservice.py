from mongoengine import *
from Objects.user import User
from Services.servicebase import ServiceBase, Result

class UserService(ServiceBase):

	def __init__(self, instancename):
		ServiceBase.__init__(self, instancename)

	def getbyemail(self, email):
		query = lambda x:User.objects(email=x).first()
		current = Result().safe_execute(query,email)

		if current.isvalid:
			self.logit("getbyemail performed", current.result.email)
		else:
			self.logit("getbyemail performed", "user not found")
		return current

	def getbyid(self, id):
		query = lambda x:User.objects(_id=x).first()
		current = Result().safe_execute(query, id)

		if current.isvalid:
			self.logit("getbyid performed", current.result.email)
		else:
			self.logit("getbyid performed", "user not found")

		return current

	def add(self, email):
		newuser = User(email=email)
		newuser.save()
		self.logit("add performed", newuser.email)
		return newuser

	def delete(self, id):
		current = getUserById(id)

		if current.isvalid:
			current.result.delete()
			self.logit("delete performed", current.result.email + " has been deleted")
		else:
			self.logit("delete performed", "user not found for deletion")
		

	def deleteall(self):
		User.drop_collection()
		self.logit("deleteall performed", " User collection has been deleted")
		