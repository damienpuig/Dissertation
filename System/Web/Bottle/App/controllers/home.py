# -*- coding: utf-8 -*-
from App import app, redis
from Services.userservice import UserService
from Services.servicebase import ServiceBase
from Services.deviceservice import DeviceService
from Services.commentservice import CommentService
from Services.valueservice import ValueService
from Objects.comment import Comment
from base import authenticated
from bottle import template, request, redirect

# TO DO : VALUE SERVICES DANS CHAQUE METHODE
user_s = UserService('UserService')
log_s = ServiceBase('ServiceBase')
device_s = DeviceService('DeviceService')
comment_s = CommentService('CommentService')
value_s = ValueService('ValueService')

@app.wrap_app.route('/', method='GET')
@authenticated
def index():
	#device12comments()
	#device21comment()
	comments('arduino1')
	log = log_s.last()
	return template('home/index', message=log.result.content + " :" + log.result.details)



def device12comments():
	user = user_s.getbyemail('damien.puig@gmail.com')
	device = device_s.getbyname(name='arduino1')

	if device is None:
		device = device_s.add('arduino1', 'this is the arduino 1', [40,30])
		print("DEVICE CREATED: " + device.name)
	else:
		print("DEVICE " + device.result.name + " ALREADY ON MONGODB")

	value = value_s.add(device, 'lum', 40.1, None)

	comment1 = Comment(content='pas mal cette value1!', author=user.result.email)
	comment2 = Comment(content='pas mal cette value2!', author=user.result.email)
	
	comment_s.adds(value.result, [comment1, comment2])

def comments(arduinoname):
	user = user_s.getbyemail('damien.puig@gmail.com')
	device = device_s.getbyname(name=arduinoname)

	value = value_s.getbydevice(device.result, 1)

	print(str(value))

	for value in value.result.values:
		print(str(value))

	comment1 = Comment(content='pas mal cette value1!', author=user.result.email)
	comment2 = Comment(content='pas mal cette value2!', author=user.result.email)
	
	print(str(comment1))

	print(str(comment2))

	comment_s.adds(value, [comment1, comment2])

def device21comment():
	user = user_s.getbyemail('damien.puig@gmail.com')
	device = device_s.getbyname(name='arduino2')

	if device is None:
		device = device_s.add('arduino2', 'this is the arduino 2', [40,30])
		print("DEVICE CREATED: " + device.name)
	else:
		print("DEVICE " + device.result.name + " ALREADY ON MONGODB")

	value = device_s.addvalue(device, 'lum', 40.1, None)

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