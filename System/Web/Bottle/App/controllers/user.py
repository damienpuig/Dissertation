# -*- coding: utf-8 -*-
from App import app
from Services.userservice import UserService
from Services.servicebase import ServiceBase
from base import authenticated
from bottle import template, request, redirect

user_s = UserService()
log_s = ServiceBase()

@app.wrap_app.route('/me', method='GET')
@authenticated
def me():
    return template('home/index', message="ME BUT PAGE NOT DONE")

@app.wrap_app.route('/new', method=['GET', 'POST'])
def new():
    if request.method == 'POST':
        enteredemail = request.forms.get('email')
        enteredpassword = request.forms.get('pass')
        newuser = user_s.addUser(enteredemail, enteredpassword)
        request.environ["beaker.session"]['email'] = newuser.email
        return template('home/index', message=newuser.email)
    return template('user/new', message='')


@app.wrap_app.route('/login', method=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.forms.get('email')
        loggeduser = user_s.getUserByEmail(email)

        if loggeduser is not None:
            request.environ["beaker.session"]['email'] = loggeduser.email
            redirect('/me')

    return template('user/login', message='')

@app.wrap_app.route('/logout', method='GET')
@authenticated
def logout():
    del request.environ["beaker.session"]['email']
    redirect('/')


@app.wrap_app.route('/deleteuser', method='GET')
@authenticated
def delete():
    user_s.removeAllUsers()
    log = log_s.getLastLog()
    return template('home/index', message=log.content + " :" + log.details)