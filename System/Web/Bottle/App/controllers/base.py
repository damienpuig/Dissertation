import os
from App import app, redis
from bottle import *


#This is the controller base.
#We declared attribute checking if the user is logged
#If not, redirect to login
def authenticated(func):
    def wrapped(*args, **kwargs):
            session = request.environ["beaker.session"]
            print request.environ["beaker.session"]
            if  session.has_key('email'):
                print('User using session: ' + session['email'])
                return func(*args, **kwargs)

            print 'Unknown user'
            redirect('/login')
    return wrapped