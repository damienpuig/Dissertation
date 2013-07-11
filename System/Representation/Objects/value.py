from mongoengine import *
from Objects.comment import Comment
import datetime

class Value(Document):
    valueType = StringField(max_length=120, required=True)
    value = FloatField(required=True)
    comments = ListField(EmbeddedDocumentField(Comment))
    date = DateTimeField(default=datetime.datetime.now)