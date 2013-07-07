# -*- coding: utf-8 -*-
from App import app, redis
from Services.userservice import UserService
from Services.servicebase import ServiceBase
from Services.deviceservice import DeviceService
from Objects.comment import Comment
from base import authenticated
from bottle import template, request, redirect

user_s = UserService('UserService')
log_s = ServiceBase('ServiceBase')
device_s = DeviceService('DeviceService')
isauth = None


@app.wrap_app.hook('after_request')
def isauthenticated():
	session = request.environ["beaker.session"]
	if session.has_key('email'):
		isauth=True
	else:
		isauth=False


@app.wrap_app.route('/', method='GET')
@authenticated
def index():

	#device_s.add('arduino1', 'this is the arduino 1', ['lum'], [40,30])
	device = device_s.getbyname(name='arduino1')
	user = user_s.getbyemail('damien.puig@gmail.com')
	print user.result.email
	newcomment = Comment(content='bien bien', author=user.result)
	#device_s.addvalue(device, 'lum', 40.1, newcomment)

	log = log_s.last()
	return template('home/index', message=log.content + " :" + log.details, isauth=isauth)