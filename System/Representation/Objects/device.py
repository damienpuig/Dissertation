import json

from mongoengine import *

from Objects.value import Value
from Objects.mongoextension import encode_model


#Device representation
class Device(Document):
    name = StringField(max_length=60, required=True)
    description = StringField(max_length=120, required=True)
    values = ListField(ReferenceField('Value', reverse_delete_rule=NULLIFY))
    location = PointField(auto_index=False, required=True)

    def tojson(self):
        return json.dumps(self, default=encode_model)