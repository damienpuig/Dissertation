from mongoengine import *

class User(Document):
    email = EmailField(required=True)
    password = StringField(required=True)

