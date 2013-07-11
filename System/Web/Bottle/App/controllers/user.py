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
    email = request.environ["beaker.session"]['email']
    currentuser = user_s.getbyemail(email)

    return template('user/me', message="this is the me page", user=currentuser.result)

@app.wrap_app.route('/new', method=['GET', 'POST'])
def new():
    if request.method == 'POST':
        newemail = request.forms.get('email')
        currentuser = user_s.add(newemail)

        request.environ["beaker.session"]['email'] = currentuser.email
        return template('home/index', message=currentuser.email)

    return template('user/new', message='')


@app.wrap_app.route('/login', method=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.forms.get('email')
        currentuser = user_s.getbyemail(email)

        if not (currentuser is None):
            request.environ["beaker.session"]['email'] = currentuser.result.email
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