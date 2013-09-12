from mongoengine import *
from Objects.mongoextension import encode_model
import json

class User(Document):
    email = EmailField(required=True)

    def tojson(self):
    	return json.dumps(self, default=encode_model)

