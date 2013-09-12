# -*- coding: utf-8 -*-
from App import app, redis
from datetime import datetime
import json, time
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

	now = datetime.today()
	values = value_s.getbytime(10, now.replace(day=now.day-3))

	return template('sensor/panel', message="this is the arduino panel page", user=currentuser.result, values=values.result)


@app.wrap_app.route('/panel/lpupdate', method='GET')
@authenticated
def panel():

	if not request.query.date:
		date = datetime.today()
	else:
		fmt = '%Y-%d-%mT%H:%M:%S'
		parts = request.query.date.split('.')
		date = datetime.strptime(parts[0], fmt)
		#little hack
		date = date.replace(microsecond=int(parts[1])+1)

	values = value_s.getbytime(10, date)

	response.content_type = 'application/json'


	def preparehtml(values):
		sb = []
		for value in values:
			sb.append(template('template/value', value=value))
		return ''.join(sb)

	if not values.result:
		return { 
		"count": values.result.count(),
		"last": date.isoformat()
		}
	else:
		return {  
		"data" : preparehtml(values.result),
		"count": values.result.count(), 
		"last": values.result[0].date.isoformat()
		}



@app.wrap_app.route('/arduino/<relatedvalueid>', method='GET')
@authenticated
def arduino(relatedvalueid):
	email = request.environ["beaker.session"]['email']
	currentuser = user_s.getbyemail(email)

	value = value_s.getbyid(relatedvalueid)

	device = device_s.getbyvalue(value.result)

	if not value.isvalid:
		return value.error
	elif not device.isvalid:
		return device.error
	else:
		print device
		return template('sensor/arduino', message="this is the arduino page", user=currentuser.result, device=device.result)