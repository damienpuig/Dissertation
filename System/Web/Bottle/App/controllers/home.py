# -*- coding: utf-8 -*-
from bottle import template

from App import app
from Services.userservice import UserService
from Services.servicebase import ServiceBase
from Services.deviceservice import DeviceService
from Services.commentservice import CommentService
from Services.valueservice import ValueService
from Objects.comment import Comment
from base import authenticated



#Services declaration
###########################################
user_s = UserService('UserService')
log_s = ServiceBase('ServiceBase')
device_s = DeviceService('DeviceService')
comment_s = CommentService('CommentService')
value_s = ValueService('ValueService')
###########################################

#ROUTE /
@app.wrap_app.route('/', method='GET')
@authenticated
def index():
    log = log_s.last()
    return template('home/index', message=log.result.content + " :" + log.result.details)


#Some tests
###########################################
def device12comments():
    user = user_s.getbyemail('damien.puig@gmail.com')
    device = device_s.getbyname(name='arduino1')

    if device is None:
        device = device_s.add('arduino1', 'this is the arduino 1', [40, 30])
        print("DEVICE CREATED: " + device.name)
    else:
        print("DEVICE " + device.result.name + " ALREADY ON MONGODB")

    value = value_s.add(device, 'lum', 40.1, [40, 30], None, None, None)

    comment1 = Comment(content='pas mal cette value1!', author=user.result.email)
    comment2 = Comment(content='pas mal cette value2!', author=user.result.email)

    comment_s.adds(value.result, [comment1, comment2])


def comments(arduinoname):
    user = user_s.getbyemail('damien.puig@gmail.com')
    device = device_s.getbyname(name=arduinoname)

    value = value_s.getbydevice(device.result, 1)

    print(str(value))

    comment1 = Comment(content='pas mal cette value1!', author=user.result.email)
    comment2 = Comment(content='pas mal cette value2!', author=user.result.email)

    print(str(comment1))

    print(str(comment2))

#comment_s.adds(value, [comment1, comment2])

def device21comment():
    user = user_s.getbyemail('damien.puig@gmail.com')
    device = device_s.getbyname(name='arduino2')

    if device is None:
        device = device_s.add('arduino2', 'this is the arduino 2', [40, 30])
        print("DEVICE CREATED: " + device.name)
    else:
        print("DEVICE " + device.result.name + " ALREADY ON MONGODB")

    value = value_s.add(device, 'lum', 40.1, [40, 30], None, None, None)

    comment1 = Comment(content='pas mal cette value1!', author=user.result.email)

    comment_s.add(value.result, comment1)


def newuser():
    user = user_s.getbyemail('damien.puig@gmail.com')
    if user is None:
        user = user_s.add('damien.puig@gmail.com')
        print("USER CREATED: " + user.result.email)
    else:
        print("USER " + user.result.email + " ALREADY ON MONGODB")
    return user
    ###########################################