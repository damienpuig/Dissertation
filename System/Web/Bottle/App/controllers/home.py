# -*- coding: utf-8 -*-
from App import app
#from Objects.user import User
#from Objects.log import Log
from Services.userservice import UserService
from Services.servicebase import ServiceBase
from base import authenticated
from bottle import template, request

user_s = UserService()
log_s = ServiceBase()


@app.wrap_app.route('/', method='GET')
def index():
    log = log_s.getLastLog()
    return template('home/index', message=log.content + " :" + log.details)