# -*- coding: utf-8 -*-
from App import app
from bottle import static_file


@app.wrap_app.route('/:file#(favicon.ico|humans.txt)#')
def favicon(file):
    return static_file(file, root='App/static/misc')


@app.wrap_app.route('/:path#(images|css|js|fonts)\/.+#')
def server_static(path):
    return static_file(path, root='App/static')
