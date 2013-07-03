import logging
from datetime import datetime

from mongoengine import *
from mongoengine import signals

def (sender, document):
    document.date = datetime.utcnow()