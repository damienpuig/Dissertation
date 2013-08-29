from mongoengine import *
import datetime

class Log(Document):
    logType = StringField(max_length=120, required=True)
    content = StringField(required=True, max_length=120)
    details = StringField(required=True, max_length=120)
    date = DateTimeField(default=datetime.datetime.now)

    @queryset_manager
    def objects(doc_cls, queryset):
    	return queryset.order_by('-date')

    def __str__(self):
    	return "{{\"logType\": \"{0}\", \"content\": \"{1}\", \"details\": \"{2}\", \"date\": \"{3}\"}}".format(self.logType, self.content, self.details, self.date)