import os

from flask import Flask
from flask import jsonify
from flask import render_template

from app.database_util import DatabaseUtil

app = Flask(__name__)

with DatabaseUtil() as db:
    db.create_user_table()
    # db.insert_user('test', '1234')

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
