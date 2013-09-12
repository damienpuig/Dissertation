from bson.objectid import ObjectId
from mongoengine import *
from types import ModuleType
from itertools import groupby 
from datetime import datetime
import json

def encode_model(obj):
    if isinstance(obj, (Document, EmbeddedDocument)):
        out = dict(obj._data)
        for k,v in out.items():
            if isinstance(v, ObjectId):
                out[k] = str(v)
    elif isinstance(obj, QuerySet):
        out = list(obj)
    elif isinstance(obj, ModuleType):
        out = None
    elif isinstance(obj, groupby):
        out = [ (g,list(l)) for g,l in obj ]
    elif isinstance(obj, (list,dict)):
        out = obj
    elif isinstance(obj, datetime):
        out = obj.isoformat()
    else:
        raise TypeError, "Could not JSON-encode type '%s': %s" % (type(obj), str(obj))
    return out