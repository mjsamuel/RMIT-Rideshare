from flask import Blueprint, render_template
from flask import current_app as app

site = Blueprint("site", __name__,
    template_folder='templates',
     static_folder='static')

@site.route('/login')
def login():
    return render_template('login.html', title='Login')

@site.route('/register')
def register():
    return render_template('register.html', title='Register')
