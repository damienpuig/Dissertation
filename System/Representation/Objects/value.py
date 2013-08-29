from mongoengine import *
from Objects.comment import Comment
import datetime

class Value(Document):
    valueType = StringField(max_length=120, required=True)
    value = FloatField(required=True)
    comments = ListField(EmbeddedDocumentField(Comment))
    date = DateTimeField(default=datetime.datetime.now)

    @queryset_manager
    def objects(doc_cls, queryset):
    	return queryset.order_by('-date')

    def __str__(self):
    	return "{{\"valueType\": \"{0}\", \"value\": \"{1}\", \"comments\": \"{2}\", \"date\": \"{3}\"}}".format(self.valueType, self.value, len(self.comments), self.date)