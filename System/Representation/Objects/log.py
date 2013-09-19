from mongoengine import *
from Objects.mongoextension import encode_model
import datetime, json

#Log representation
class Log(Document):
    logType = StringField(max_length=120, required=True)
    content = StringField(required=True)
    details = StringField(required=True)
    date = DateTimeField(default=datetime.datetime.now)

    @queryset_manager
    def objects(doc_cls, queryset):
    	return queryset.order_by('-date')

    def tojson(self):
    	return json.dumps(self, default=encode_model)