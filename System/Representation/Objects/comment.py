from mongoengine import *
from Objects.user import User
from Objects.mongoextension import encode_model
import datetime, json

#Comment is an embedded entity in the value object.
class Comment(EmbeddedDocument):
    content = StringField(required=True)
    author = EmailField(required=True)
    date = DateTimeField(default=datetime.datetime.now)

    @queryset_manager
    def objects(doc_cls, queryset):
    	return queryset.order_by('-date')

    def tojson(self):
    	return json.dumps(self, default=encode_model)