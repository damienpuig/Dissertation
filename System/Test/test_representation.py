from __future__ import with_statement
import pytest, datetime
from mongoengine import *
from Objects.device import Device
from Objects.value import Value
from Objects.user import User
from Objects.log import Log
from Objects.comment import Comment
from Objects.qoc import QoC
import redis



class TestRepresentation(object):

    def test_representation_device(self, r):

    	assert isinstance(Device(name="arduino1", description="blabla", values=None, location=[34,45]), Device) == True


    def test_representation_value(self, r):
    	newQoC = QoC(completeness = 0.8, significance = "low")
    	assert isinstance(Value(valueType= "lala", value= 1.0, comments = None, date = datetime.datetime.now(), location = [45, 55], qoc = newQoC), Value) == True



    def test_representation_user(self, r):

    	assert isinstance(User(email="damien.puig@gmail.com"), User) == True



    def test_representation_log(self, r):
    	assert isinstance(Log(logType= "ERROR",  content = "lalala", details ="lalala", date = datetime.datetime.now()), Log) == True