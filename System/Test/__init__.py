import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..\Representation'))

from mongoengine import *

register_connection("default", name='dissertation-test', host='localhost', port=27017)