from mongoengine import *
from Objects.user import User

class Comment(Document):
    content = StringField()
    author = ReferenceField(User)
    date = DateTimeField(default=datetime.datetime.now)