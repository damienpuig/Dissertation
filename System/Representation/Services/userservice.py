from mongoengine import *
from Objects.user import User
from Services.servicebase import ServiceBase

class UserService(ServiceBase):
	def getUserByEmail(self, email):
		current = User.objects(email=email).first()
		self.logIt("getuserbyemail performed", current.email)
		return current

	def getUserById(self, id):
		current = User.objects(_id=id).first()
		self.logIt("getUserById performed", current.email)
		return current

	def addUser(self, email, password):
		newuser = User(email=email, password=password)
		newuser.save()
		self.logIt("addUser performed", newuser.email)
		return newuser

	def removeUserById(self, id):
		current = getUserById(id)
		current.delete()
		self.logIt("removeUserById performed", current.email + " has been deleted")
		pass

	def removeAllUsers(self):
		User.drop_collection()
		self.logIt("removeAllUsers performed", " User collection has been deleted")
		pass