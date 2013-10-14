# -*- coding: utf-8 -*-
from datetime import datetime

from bottle import template, request, response

from App import app
from Services.userservice import UserService
from Services.servicebase import ServiceBase
from Services.deviceservice import DeviceService
from Services.valueservice import ValueService
from base import authenticated



#Service declaration
###########################################
user_s = UserService('UserService')
log_s = ServiceBase('ServiceBase')
device_s = DeviceService('DeviceService')
value_s = ValueService('ValueService')
###########################################

#ROUTE /panel
@app.wrap_app.route('/panel', method='GET')
@authenticated
def panel():
    email = request.environ["beaker.session"]['email']
    currentuser = user_s.getbyemail(email)

    now = datetime.today()
    values = value_s.getbytime(10, now.replace(day=now.day - 3))

    return template('sensor/panel', message="this is the arduino panel page", user=currentuser.result,
                    values=values.result)

#ROUTE /panel/lpupdate
#This route is only called from long polling action, asynchronously
@app.wrap_app.route('/panel/lpupdate', method='GET')
@authenticated
def panel():
    #We check the sended date
    if not request.query.date:
        date = datetime.today()
    else:
        fmt = '%Y-%m-%dT%H:%M:%S'
        parts = request.query.date.split('.')
        date = datetime.strptime(parts[0], fmt)
        #little hack
        date = date.replace(microsecond=int(parts[1]) + 1)

    #We get the value using the value service
    values = value_s.getbytime(10, date)

    response.content_type = 'application/json'

    #Compute the values in HTML
    def preparehtml(values):
        sb = []
        for value in values:
            sb.append(template('template/value', value=value))
        return ''.join(sb)

    # sends computed json response (0 work on client side, which are mobiles)
    if not values.result:
        return {
            "count": values.result.count(),
            "last": date.isoformat()
        }
    else:
        return {
            "data": preparehtml(values.result),
            "count": values.result.count(),
            "last": values.result[0].date.isoformat()
        }


#ROUTE /arduino/idofthevaluethatcalledforthearduino
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
        return template('sensor/arduino', message="this is the arduino page", user=currentuser.result,
                        device=device.result)