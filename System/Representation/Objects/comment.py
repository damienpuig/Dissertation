from mongoengine import *
from Objects.user import User
import datetime

class Comment(EmbeddedDocument):
    content = StringField(required=True)
    author = EmailField(required=True)
    date = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
    	return "{{\"content\": \"{0}\", \"author\": \"{1}\", \"date\": \"{2}\"}}".format(self.content, self.author, self.date)