from mongoengine import *
from Objects.comment import Comment
from Objects.device import Device

class Value(Document):
    valueType = StringField(max_length=120, required=True)
    value = FloatField()
    device = ReferenceField("Device", reverse_delete_rule=mongoengine.DO_NOTHING)
    Comments = ListField(EmbeddedDocumentField(Comment))
    date = DateTimeField(default=datetime.datetime.now)

