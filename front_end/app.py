# import pytest
from gevent.pywsgi import WSGIServer
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap4
import os
import shutil
from wtforms.fields import *
from wtforms.validators import DataRequired, Length
from wtforms import StringField, SubmitField, BooleanField, PasswordField, IntegerField,  \
    FormField, SelectField, FieldList
from flask_wtf import FlaskForm, CSRFProtect
from flask import send_file, send_from_directory, make_response
from flask import Flask, render_template, request, flash, Markup, jsonify
from werkzeug.security import check_password_hash
import requests
from flask_cors import CORS
import json

# from uuid import uuid3, NAMESPACE_DNS
# from flask_login import UserMixin
# import pymysql

# from Users import Users, LoginForm, RegisterForm


app = Flask(__name__)
CORS(app, resources=r'/*')
app.secret_key = 'dev'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

# set default button sytle and size, will be overwritten by macro parameters
app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
app.config['BOOTSTRAP_BTN_SIZE'] = 'sm'
app.config['UPLOAD_FOLDER'] = 'storage/'
# app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'lumen'  # uncomment this line to test bootswatch theme

bootstrap = Bootstrap4(app)
db = SQLAlchemy(app)
# csrf = CSRFProtect(app)


@app.route('/')
def hello_world():
    return render_template('upload.html')


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/waiting', methods=['POST'])
def waiting():
    if request.method == 'POST':
        # print(request.files)
        # 先清空文件夹
        storagepath = os.path.join(app.config['UPLOAD_FOLDER'])
        shutil.rmtree(storagepath)
        os.mkdir(storagepath)
        # 命名统一使用英文，防止源文件中有中文导致命名失败
        xml1 = request.files['xml1']
        xml1.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename('a.xml')))
        img1 = request.files['img1']
        img1.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename('b.png')))
        xml2 = request.files['xml2']
        xml2.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename('c.xml')))
        img2 = request.files['img2']
        img2.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename('d.png')))

        # file_info = FileInfo(old_apk.filename, new_apk.filename, old_script.filename)

        return render_template('waiting.html')
    else:
        return 'file uploaded failed'


@app.route('/result')
def show_result():
    sim = request.args.get("sim")
    print(sim)
    return render_template('result.html', sim=sim)
    

if __name__ == '__main__':
    # app.debug = True
    # app.threaded = True
    # WSGIServer(("0.0.0.0", 5001), app).serve_forever()
    app.run(host="127.0.0.1", port=5001, debug=True, threaded=True)
