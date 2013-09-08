# -*- coding: utf-8 -*-
from App import app, redis
import datetime
import json
from Services.userservice import UserService
from Services.servicebase import ServiceBase
from Services.deviceservice import DeviceService
from Services.valueservice import ValueService
from Objects.comment import Comment
from base import authenticated
from bottle import template, request, redirect, response

user_s = UserService('UserService')
log_s = ServiceBase('ServiceBase')
device_s = DeviceService('DeviceService')
value_s = ValueService('ValueService')

@app.wrap_app.route('/panel', method='GET')
@authenticated
def panel():
	email = request.environ["beaker.session"]['email']
	currentuser = user_s.getbyemail(email)

	now = datetime.datetime.today()
	values = value_s.getbytime(10, now.replace(day=now.day-3))

	print values

	return template('sensor/panel', message="this is the arduino panel page", user=currentuser.result, values=values.result)


@app.wrap_app.route('/panel/lpupdate', method='GET')
@authenticated
def panel():

	date = request.query.get("date")

	if not (date is None):
		now = datetime.datetime.today()
		date = now.replace(hour=now.hour-1)


	values = value_s.getbytime(10, date)

	response.content_type = 'application/json'

	def preparehtml(values):
		sb = []
		for value in values:
			sb.append(template('template/value', value=value))
		return ''.join(sb)

	return { "success" : True, "data" : preparehtml(values.result), "last": values.result[0].date.isoformat()}




@app.wrap_app.route('/arduino', method='GET')
@authenticated
def arduino():
	email = request.environ["beaker.session"]['email']
	currentuser = user_s.getbyemail(email)

	proposedid = request.query['value']

	value = value_s.getbyid(proposedid)

	device = device_s.getbyvalue(value.result)

	if not value.isvalid:
		return value.error
	elif not device.isvalid:
		return device.error
	else:
		print device
		return template('sensor/arduino', message="this is the arduino page", user=currentuser.result, device=device.result)