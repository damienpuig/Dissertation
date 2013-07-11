from mongoengine import *
import datetime

class Log(Document):
    logType = StringField(max_length=120, required=True)
    content = StringField(required=True, max_length=120)
    details = StringField(required=True, max_length=120)
    date = DateTimeField(default=datetime.datetime.now)