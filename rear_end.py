import json
import os
import shelve
from datetime import datetime
from random import random

from flask import Flask, request
from flask_cors import CORS
import xmlSim

# q = queue.Queue(1)
app = Flask(__name__)
CORS(app, resources=r'/*')
app.secret_key = 'dev'

classList = {}


def getClass(str):
    """
    将 class + bounds 的组合还原出 class
    :param str: class + bounds
    :return: class
    """
    return str.split('[')[0]


@app.route('/calculate')
def calculate():
    global classList
    sim, classList = xmlSim.xmlSim()
    print(sim)
    res = {'sim': sim}
    return json.dumps(res)


@app.route('/getList')
def getList():
    js = []
    global classList
    for key, value in classList.items():
        js.append({'src': getClass(key), 'dst': getClass(value)})
    return json.dumps(js)


# dev version
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=12300, debug=True, threaded=True)
