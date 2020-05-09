from flask import Blueprint, render_template, request
import requests, json
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
    return render_template('search_cars.html', title='Cars')

@site.route('/car')
def book_car():
    carId = request.args.get('id')
    response = requests.get('http://localhost:5000/api/cars?id=' + carId)
    data = json.loads(response.text)
    title = data['cars']['make'] + ' - ' + data['cars']['body_type']

    return render_template('book_car.html', title=title, car=data['cars'])
