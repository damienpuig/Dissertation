from __future__ import with_statement
import pytest, redis, datetime
from mongoengine import *
from Objects.device import Device
from Objects.value import Value
from Objects.user import User
from Objects.log import Log
from Objects.comment import Comment
from Objects.qoc import QoC


class TestStoring(object):

    def test_store_retreive_device(self, r):
    	newDevice = Device(name="arduino40", description="blabla", values=None, location=[34,45])
    	assert newDevice.save()




    def test_store_retreive_value(self, r):
    	newQoC = QoC(completeness = 0.8, significance = "low")
    	newValue = Value(valueType= "lala", value= 1.0, comments = None, date = datetime.datetime.now(), location = [45, 55], qoc = newQoC)
    	assert newValue.save()




    def test_store_retreive_user(self, r):
    	newUser = User(email="dg@gmail.com")
    	assert newUser.save()




    def test_store_retreive_last_log(self, r):
        newLog = Log(logType= "ERROR",  content = "lalala", details ="lalala", date = datetime.datetime.now())
    	assert newLog.save()