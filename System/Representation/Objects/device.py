from mongoengine import *

class Device(Document):
	name = StringField(max_length=60)
    description = StringField(max_length=120, required=True)
    sensors = ListField(StringField(max_length=30))
    values = ListField(ReferenceField("Value", reverse_delete_rule=mongoengine.NULLIFY))
    location = PointField(auto_index=False)