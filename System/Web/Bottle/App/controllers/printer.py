# -*- coding: utf-8 -*-
from App import app
from bottle import template, request


@app.route('/', method='GET')
def index():
    return template('printer/index', message='')


@app.route('/print', method=['GET', 'POST'])
def printer():
    if request.method == 'POST':
        from App.models.Printer import Printer
        printer = Printer()
        message = printer.show_string(request.forms.get('text'))
        return template('printer/index', message=message)
    return template('printer/print', message='')
