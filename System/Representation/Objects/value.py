import datetime
import json

from mongoengine import *

from Objects.comment import Comment
from Objects.qoc import QoC
from Objects.mongoextension import encode_model


#Value representation
class Value(Document):
    valueType = StringField(max_length=120, required=True)
    value = FloatField(required=True)
    comments = ListField(EmbeddedDocumentField(Comment))
    date = DateTimeField(default=datetime.datetime.now)
    location = PointField(auto_index=False, required=True)
    qoc = EmbeddedDocumentField(QoC)

    @queryset_manager
    def objects(doc_cls, queryset):
        return queryset.order_by('-date')


    def tojson(self):
        return json.dumps(self, default=encode_model)