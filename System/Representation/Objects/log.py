from mongoengine import *
import datetime

class Log(Document):
    logType = StringField(max_length=120, required=True)
    content = StringField()
    details = StringField()
    date = DateTimeField(default=datetime.datetime.now)