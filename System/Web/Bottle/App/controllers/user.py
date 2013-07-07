# -*- coding: utf-8 -*-
from App import app, redis
from Services.userservice import UserService
from Services.servicebase import ServiceBase
from base import authenticated
from bottle import template, request, redirect

user_s = UserService('UserService')
log_s = ServiceBase('ServiceBase')



@app.wrap_app.route('/me', method='GET')
@authenticated
def me():
    print 'me'
    return template('user/me', message="ME BUT PAGE NOT DONE")

@app.wrap_app.route('/new', method=['GET', 'POST'])
def new():
    if request.method == 'POST':
        enteredemail = request.forms.get('email')
        newuser = user_s.add(enteredemail)

        request.environ["beaker.session"]['email'] = newuser.email
        #redis.set(newuser.email, request.environ["beaker.session"])
        return template('home/index', message=newuser.email)
    return template('user/new', message='')


@app.wrap_app.route('/login', method=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.forms.get('email')
        loggeduser = user_s.getbyemail(email)

        if loggeduser is not None:
            request.environ["beaker.session"]['email'] = loggeduser.result.email
            print request.environ["beaker.session"]['email']
            redirect('/me')

    return template('user/login', message='')

@app.wrap_app.route('/logout', method='GET')
@authenticated
def logout():
    request.environ["beaker.session"].delete()
    redirect('/')


@app.wrap_app.route('/deleteuser', method='GET')
@authenticated
def delete():
    user_s.deleteall()
    log = log_s.last()
    return template('home/index', message=log.content + " :" + log.details)