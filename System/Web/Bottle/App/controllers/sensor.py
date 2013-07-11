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

@app.wrap_app.route('/panel', method='GET')
@authenticated
def panel():
	email = request.environ["beaker.session"]['email']
	currentuser = user_s.getbyemail(email)
	return template('arduino/panel', message="this is the arduino panel page", user=currentuser.result)