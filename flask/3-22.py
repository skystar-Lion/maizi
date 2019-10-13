# -*- coding=utf-8 -*-
from flask import Flask,render_template,request,redirect,url_for,make_response
from werkzeug.routing import BaseConverter
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
import os

class RegexConverter(BaseConverter):
    """docstring for RegexConverter"""
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]



app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter
Bootstrap(app)

@app.route('/regex/<regex("[a-z]{3}"):uuid>')
def get_uuid(uuid):
    return "uuid:%s" % uuid 

@app.route('/')
def hello_world():
    resp = make_response(render_template('base.html'))
    resp.set_cookie("username", "the username")
    return resp

@app.route('/baidu/')
def baidu():
    return 'baidu'

@app.route('/google')
def google():
    return 'google'

@app.route('/usr/<username>')
def show_username(username):
    return 'user: %s' % username

@app.route('/post/<int:year>')
def show_year(year):
    return 'year: %d' % year


def passdo_the_login():
    return 'post'

def show_login_form():
    return 'get'


@app.route('/login', methods = ['get', 'post'])
def login():
    return render_template('login.html', method = request.method)


@app.route('/hello')
@app.route('/hello/<name>')
def hello(name = None):
    return render_template('hello.html', name = name)

@app.route('/service')
def services():
    return 'service'

@app.route('/about')
def abouts():
    return 'about'

@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.abspath(os.path.dirname(__file__))
        upload_path = os.path.join(basepath, 'upload')
        f.save(upload_path + '/' + secure_filename(f.filename))
        return redirect(url_for('upload'))
    return render_template('upload.html')




if __name__ == "__main__":
    app.run(debug = True)