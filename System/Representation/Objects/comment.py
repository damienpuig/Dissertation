from mongoengine import *
from Objects.user import User
import datetime

class Comment(EmbeddedDocument):
    content = StringField()
    author = ReferenceField(User)
    date = DateTimeField(default=datetime.datetime.now)