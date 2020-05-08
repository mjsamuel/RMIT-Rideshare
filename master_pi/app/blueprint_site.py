from flask import Blueprint, render_template, request
from app.extensions import ma

site = Blueprint("site", __name__,
    template_folder='templates',
    static_folder='static')

@site.route('/login')
def login():
    return render_template('login.html', title='Login')

@site.route('/register')
def register():
    return render_template('register.html', title='Register')

@site.route('/')
def booked_cars():
    return render_template('booked_cars.html', title='Booked Cars')

@site.route('/cars')
def search_cars():
    return render_template('search_cars.html', title='Cars', cars=None)
