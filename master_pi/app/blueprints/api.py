from datetime import datetime, timedelta
from flask import Blueprint, current_app, jsonify, request

from app.extensions import db, ma, bcrypt
from app.models.user import User, user_schema
from app.models.car import Car, car_schema
from app.models.booking import Booking, booking_schema

api = Blueprint("api", __name__, url_prefix='/api')

@api.route('/login', methods = ["POST"])
def login():
    """Endpoint for a user's credentials to be checked in order to log in to their account

    .. :quickref: User; Validate user credentials for login.

    **Example request**:

    .. sourcecode:: http

        POST /api/login HTTP/1.1
        Host: localhost
        Accept: application/json
        Content-Type: application/json

        {
            "username": "dummy",
            "password": "abcd"
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "message": "Logged in successfully",
            "user": {
                "username": "dummy"
            }
        }

    .. sourcecode:: http

        HTTP/1.1 401 UNAUTHORIZED
        Content-Type: application/json

        {
            "message": "Incorrect password",
            "user": null
        }

    :<json string username: unique username
    :<json string password: password for specified account
    :>json message: repsonse information such as error information
    :>json app.models.user.User user: the user object that has been created
    :resheader Content-Type: application/json
    :status 200: successful login
    :status 400: malformed request
    :status 401: incorrect password
    :status 404: user does not exist
    """

    response = {
        'message': '',
        'user': None
    }
    status = None

    if ('username' not in request.json) or (request.json["username"] == ""):
        response['message'] = "Missing username"
        status = 400
    elif ('password' not in request.json) or (request.json["password"] == ""):
        response['message'] = "Missing password"
        status = 400
    else:
        username = request.json["username"]
        password = request.json["password"]

        user = User.query.get(username)
        if user is None:
            response['message'] = "User does not exist"
            status = 404
        else:
            password_match = bcrypt.check_password_hash(user.password, password)
            if password_match:
                response['message'] = "Logged in successfully"
                response['user'] = user_schema.dump(user)
                status = 200
            else:
                response['message'] = "Incorrect password"
                status = 401

    return response, status

@api.route('/user', methods=["POST"])
def register_user():
    """Creates a user account that does not already exist

    .. :quickref: User; Create new user.

    **Example request**:

    .. sourcecode:: http

        POST /api/user HTTP/1.1
        Host: localhost
        Accept: application/json
        Content-Type: application/json

        {
            "username": "dummy",
            "password": "abcd",
            "confirm_password": "abcd"
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "message": "Registered user successfully",
            "user": {
                "username": "dummy"
            }
        }

    .. sourcecode:: http

        HTTP/1.1 400 BAD REQUEST
        Content-Type: application/json

        {
            "message": "Passwords do not match",
            "user": null
        }

    :<json string username: username that does not already exist within the database
    :<json string password: password for new accoutn
    :<json string confirm_password: retyped password which should match the previous password value
    :>json message: repsonse information such as error information
    :>json app.models.user.User user: the user object that has been created
    :resheader Content-Type: application/json
    :status 200: successful registration
    :status 400: malformed request
    """

    response = {
        'message': '',
        'user': None
    }
    status = None

    if ('username' not in request.json) or (request.json["username"] == ""):
        response['message'] = "Missing username"
        status = 400
    elif ('password' not in request.json) or (request.json["password"] == ""):
        response['message'] = "Missing password"
        status = 400
    elif ('confirm_password' not in request.json) or (request.json["confirm_password"] == ""):
        response['message'] = "Missing confirmed password"
        status = 400
    else:
        username = request.json["username"]
        password = request.json["password"]
        confirm_password = request.json["confirm_password"]

        if password != confirm_password:
            response['message'] = "Passwords do not match"
            status = 400
        else:
            # Querying database to check if user already exists in the system
            if User.query.get(username) is not None:
                response['message'] = "User already exists"
                status = 400
            else:
                # Hashing password using brcypt's one-way encryption
                hashed_password = bcrypt.generate_password_hash(password)

                new_user = User(username, hashed_password)
                db.session.add(new_user)
                db.session.commit()

                response['message'] = "Registered user successfully"
                response['user'] = user_schema.dump(new_user)
                status = 200

    return response, status


@api.route('/user', methods=["GET"])
def get_user():
    """Gets a user from the database

    .. :quickref: User; Get a user.

    **Example request**:

    .. sourcecode:: http

        GET /api/user?username=dummy HTTP/1.1
        Host: localhost
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "message": "User found",
            "user": {
                "username": "dummy"
            }
        }

    .. sourcecode:: http

        HTTP/1.1 404 NOT FOUND
        Content-Type: application/json

        {
            "message": "User not found",
            "user": null
        }

    :query username: the username that you are searching for
    :>json message: repsonse information such as error information
    :>json app.models.user.User user: the user object found
    :resheader Content-Type: application/json
    :status 200: user found
    :status 404: user does not exit
    """

    response = {
        'message': '',
        'user': None
    }
    status = None

    username = request.args.get('username')
    user = User.query.get(username)
    if user is None:
        response['message'] = "User not found"
        status = 404
    else:
        response['message'] = "User found"
        response['user'] = user_schema.dump(user)
        status = 200

    return response, status

@api.route('/cars', methods=["GET"])
def get_cars():
    """Gets a single car or collection of cars based on the search criteria

    .. :quickref: Car; Get a collection of cars.

    **Example request**:

    .. sourcecode:: http

        GET /api/user?make=Toyota HTTP/1.1
        Host: localhost
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "message":
            "cars": [
                {
                    "body_type": "SUV",
                    "colour": "Black",
                    "cost_per_hour": 15,
                    "id": 1,
                    "location": null,
                    "make": "Toyota",
                    "no_seats": 5
                },
                {
                    "body_type": "Hatchback",
                    "colour": "Black",
                    "cost_per_hour": 15,
                    "id": 3,
                    "location": null,
                    "make": "Toyota",
                    "no_seats": 5
                }
            ]
        }

    :query id: id of the car
    :query make: make of the car
    :query body_type: body_type of the car
    :query colour:  colour of the car
    :query no_sears: number of seats in car
    :query cost_per_hour: cost per hpur to rent the car
    :>json message: repsonse information such as error information
    :>json app.models.car.Car car: the car objects found
    :resheader Content-Type: application/json
    :status 200: cars found
    """

    response = {
        'message': '',
        'cars': None
    }
    status = None

    if (request.args.get('id') is not None):
        id = request.args.get('id')
        car = Car.query.get(id)

        response['cars'] = car_schema.dump(car)
        status = 200
    else:
        cars = None
        if (request.args.get('make') is not None):
            make = request.args.get('make')
            cars = Car.query.filter_by(make=make).all()
        elif (request.args.get('body_type') is not None):
            body_type = request.args.get('body_type')
            cars = Car.query.filter_by(body_type=body_type).all()
        elif (request.args.get('colour') is not None):
            colour = request.args.get('colour')
            cars = Car.query.filter_by(colour=colour).all()
        elif (request.args.get('no_seats') is not None):
            no_seats = request.args.get('no_seats')
            cars = Car.query.filter_by(no_seats=no_seats).all()
        elif (request.args.get('cost_per_hour') is not None):
            cost_per_hour = request.args.get('cost_per_hour')
            cars = Car.query.filter_by(cost_per_hour=cost_per_hour).all()
        else:
            cars = Car.query.all()
        response['cars'] = car_schema.dump(cars, many=True)
        status = 200

    return response, status

@api.route('/booking', methods=['GET'])
def get_bookings():
    """Get a collection of bookings a user has made

    .. :quickref: Booking; Get bookings for a user.

    **Example request**:

    .. sourcecode:: http

        GET /api/booking?username=dummy HTTP/1.1
        Host: localhost
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "bookings": [
                {
                    "id": 4,
                    "car_id": 1,
                    "username": "dummy",
                    "book_time": "2020-05-09T13:38:17",
                    "duration": 2,
                    "car": {
                        "make": "Tesla,",
                        "body_type", "Pickup"
                        "...": "..."
                    }
                }
            ]
        }

    :query username: the username to filter by for bookings
    :resheader Content-Type: application/json
    :status 200: bookings found
    """
    response = {
        'bookings': None
    }

    # Getting bookings ordered from most recent, to least recent
    username = request.args.get('username')
    bookings = (Booking.query
        .filter_by(username=username)
        .order_by(Booking.book_time.desc())
        .all())

    # Adding the the car associated with the bookings to be searlized along
    # with them
    for booking in bookings:
        booking.car = Car.query.get(booking.car_id)

    response['bookings'] = booking_schema.dump(bookings, many=True)

    return response, 200

@api.route('/booking', methods=['POST'])
def make_booking():
    """Creates a user booking for a car if it isn't already booked

    .. :quickref: Booking; Make a booking.

    **Example request**:

    .. sourcecode:: http

        POST /api/booking HTTP/1.1
        Host: localhost
        Accept: application/json
        Content-Type: application/json

        {
            "car_id": 1,
            "username": "dummy",
            "duration": 3
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "message": "Success"
        }

    .. sourcecode:: http

        HTTP/1.1 401 UNAUTHORIZED
        Content-Type: application/json

        {
            "message": "Car is currently booked",
        }

    :<json string car_id: the id of the car being booked
    :<json string username: the username of the user booking the car
    :<json string duration: how long the car will be booked for in hours
    :>json message: repsonse information such as error information
    :resheader Content-Type: application/json
    :status 200: successful booking
    :status 400: malformed request
    :status 401: car is already booked
    """

    response = {
        'message': None,
    }
    status = None

    if ('duration' not in request.json) or (request.json["duration"] == "") :
        response['message'] = "Missing duration"
        status = 400
    else:
        car_id = request.json["car_id"]
        username = request.json["username"]
        duration = request.json["duration"]
        book_time = datetime.utcnow()

        # Below code block will be checking if the car is currently booked
        currently_booked = False
        # Getting most recent booking from the database
        prev_booking = (Booking.query
            .filter_by(car_id=car_id)
            .order_by(Booking.book_time.desc())
            .first())
        if (prev_booking is not None):
            # Calculating the end time for the previous booking
            prev_end_time = prev_booking.book_time + timedelta(hours=prev_booking.duration)
            # Checking if the time being booked is after the end time
            if (book_time < prev_end_time):
                currently_booked = True
                response['message'] = "Car is currently booked"
                status = 401

        # Adding booking to database if car is not currently booked
        if not currently_booked:
            booking = Booking(car_id, username, book_time, duration)
            db.session.add(booking)
            db.session.commit()
            response['message'] = "Success"
            status = 200

    return response, status

@api.route('/booking', methods=['DELETE'])
def delete_booking():
    """Deletes a booking from the database by suppling its id

    .. :quickref: Booking; Delete a booking.

    **Example request**:

    .. sourcecode:: http

        DELETE /api/booking?id=1 HTTP/1.1
        Host: localhost

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK

    :query id: the id of the booking to be deleted
    :status 200: booking deleted
    """


    id = request.args.get('id')
    booking = Booking.query.get(id)
    db.session.delete(booking)
    db.session.commit()

    return '', 200
