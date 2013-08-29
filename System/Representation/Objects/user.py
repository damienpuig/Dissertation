from mongoengine import *

class User(Document):
    email = EmailField(required=True)

    def __str__(self):
    	return "{{\"email\": \"{0}\"}}".format(self.email)

