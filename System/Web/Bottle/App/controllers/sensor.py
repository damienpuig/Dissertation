# -*- coding: utf-8 -*-
from App import app, redis
import datetime
from Services.userservice import UserService
from Services.servicebase import ServiceBase
from Services.deviceservice import DeviceService
from Services.valueservice import ValueService
from Objects.comment import Comment
from base import authenticated
from bottle import template, request, redirect

user_s = UserService('UserService')
log_s = ServiceBase('ServiceBase')
device_s = DeviceService('DeviceService')
value_s = ValueService('ValueService')

@app.wrap_app.route('/panel', method='GET')
@authenticated
def panel():
	email = request.environ["beaker.session"]['email']
	currentuser = user_s.getbyemail(email)
	date = datetime.datetime.today()
	date2 = date.replace(hour=date.hour-5)
	print date2

	values = value_s.getbytime(10, date2)

	print values

	if values.isvalid:
		print values.result

	return template('arduino/panel', message="this is the arduino panel page", user=currentuser.result, values=values.result)