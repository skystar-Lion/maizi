# -*- coding=utf-8 -*-
from flask import Flask, render_template
from livereload import Server

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title = '<h1>hello-world</h1>')

if __name__ == '__main__':
     liver_server = Server(app.wsgi_app)
     liver_server.watch('**/.*')
     liver_server.serve(open_url = True) 