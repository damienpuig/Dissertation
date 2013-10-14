import json

from mongoengine import *

from Objects.mongoextension import encode_model


#User representation
#No password inplementation needed in the dissertation.
class User(Document):
    email = EmailField(required=True)

    def tojson(self):
        return json.dumps(self, default=encode_model)

