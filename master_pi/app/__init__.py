import os

from flask import Flask
from flask import jsonify
from flask import render_template

import configparser

app = Flask(__name__)

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), os.pardir, 'config.ini'))

# Frontend HTML
@app.route('/login')
def login_page():
    return render_template('login.html', title='Login')

@app.route('/register')
def register_page():
    return render_template('register.html', title='Register')

# RESTful API
@app.route('/api/login')
def login():
    ret_value = {'message': 'Correct credentials'}
    return jsonify(ret_value)

@app.route('/api/register')
def register():
    ret_value = {'message': 'Account created'}
    return jsonify(ret_value)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
