import os
from App import app
from bottle import *


def authenticated(func):
    def wrapped(*args, **kwargs):
        session = request.environ["beaker.session"]
        print(session)

        if 'email' in session:
            return func(*args, **kwargs)
        else:
            redirect('/login')

    return wrapped