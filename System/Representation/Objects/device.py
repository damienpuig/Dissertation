from mongoengine import *
from Objects.value import Value

class Device(Document):
	name = StringField(max_length=60, required=True)
	description = StringField(max_length=120, required=True)
	values = ListField(ReferenceField('Value', reverse_delete_rule=NULLIFY))
	location = PointField(auto_index=False)