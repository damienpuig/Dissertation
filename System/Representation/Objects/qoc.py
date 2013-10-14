import json

from mongoengine import *

from Objects.mongoextension import encode_model


#Quality of Context representation for a value
class QoC(EmbeddedDocument):
    completeness = FloatField(required=True)
    significance = StringField(required=True)

    def tojson(self):
        return json.dumps(self, default=encode_model)