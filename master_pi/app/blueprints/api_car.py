from flask import Blueprint, request
from datetime import datetime

from app.extensions import db
from app.models.user import User, Role
from app.models.car import Car, car_schema
from app.models.booking import Booking
from app.forms import EditCarFormSchema

car = Blueprint("car", __name__, url_prefix='/api')

@car.route('/car', methods=["POST"])
def new_car():
    """Registers a new car if the user making the request is an admin

    .. :quickref: Car; Register a new car.

    **Example request**:

    .. sourcecode:: http

        POST /api/car HTTP/1.1
        Host: localhost
        Accept: application/json
        Content-Type: application/json

        {
            "username": "admin",
            "make": "Toyota",
            "body_type": "SUV",
            "colour": "Black",
            "no_seats": 5,
            "location": "-37.808880,144.965179",
            "cost_per_hour": 15
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
            "message": {
                "user": ["User is not an admin."]
            }
        }

    :<json string username: the username of the person updating the car
    :<json string make: the make of the car being updated
    :<json string body_type: the body_type of the car being updated
    :<json string colour: the colour of the car being updated
    :<json int no_seats: the no_seats of the car being updated
    :<json string location: the location of the car being updated
    :<json int cost_per_hour: the cost_per_hour of the car being updated
    :>json message: repsonse information such as error information
    :resheader Content-Type: application/json
    :status 200: creating a new car was successful
    :status 400: missing or invalid fields
    :status 401: user is not an admin
    """

    response = {
        'message': '',
    }
    status = 200

    form_schema = EditCarFormSchema()
    form_errors = form_schema.validate(request.json)
    if form_errors:
        response['message'] = form_errors
        status = 400
    else:
        # Checking if user making the request is an admin
        user = User.query.get(request.json["username"])
        if user.role is not Role.admin:
            response['message'] = {
                'user': ['User is not an admin.']
            }
            status = 401
        else:
            make = request.json["make"]
            body_type = request.json["body_type"]
            colour = request.json["colour"]
            no_seats = request.json["no_seats"]
            location = request.json["location"]
            cost_per_hour = request.json["cost_per_hour"]

            car = Car(make, body_type, colour, no_seats, cost_per_hour, location)
            db.session.add(car)
            db.session.commit()
            response['message'] = "Success"

    return response, status


@car.route('/car', methods=["PUT"])
def put_car():
    """Updates the data of a single car only if the user making the request is an admin

    .. :quickref: Car; Update a car.

    **Example request**:

    .. sourcecode:: http

        PUT /api/car HTTP/1.1
        Host: localhost
        Accept: application/json
        Content-Type: application/json

        {
            "car_id": 1,
            "username": "admin",
            "make": "Toyota",
            "body_type": "SUV",
            "colour": "Black",
            "no_seats": 5,
            "location": "-37.808880,144.965179",
            "cost_per_hour": 15
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
            "message": {
                "user": ["User is not an admin."]
            }
        }

    :<json string car_id: the id of the car being updated
    :<json string username: the username of the person updating the car
    :<json string make: the make of the car being updated
    :<json string body_type: the body_type of the car being updated
    :<json string colour: the colour of the car being updated
    :<json int no_seats: the no_seats of the car being updated
    :<json string location: the location of the car being updated
    :<json int cost_per_hour: the cost_per_hour of the car being updated
    :>json message: repsonse information such as error information
    :resheader Content-Type: application/json
    :status 200: updating car was successful
    :status 400: missing or invalid fields
    :status 401: user is not an admin
    """

    response = {
        'message': '',
    }
    status = 200

    form_schema = EditCarFormSchema()
    form_errors = form_schema.validate(request.json)
    if form_errors:
        response['message'] = form_errors
        status = 400
    else:
        # Checking if user making the request is an admin
        user = User.query.get(request.json["username"])
        if user.role is not Role.admin:
            response['message'] = {
                'user': ['User is not an admin.']
            }
            status = 401
        else:
            car = Car.query.get(request.json["car_id"])
            car.make = request.json["make"]
            car.body_type = request.json["body_type"]
            car.colour = request.json["colour"]
            car.no_seats = request.json["no_seats"]
            car.location = request.json["location"]
            car.cost_per_hour = request.json["cost_per_hour"]
            db.session.commit()
            response['message'] = "Success"

    return response, status


@car.route('/car', methods=["DELETE"])
def delete_car():
    """Delete a car from the database only if the user making the request is an admin

    .. :quickref: Car; Delete a car.

    **Example request**:

    .. sourcecode:: http

        DELETE /api/car HTTP/1.1
        Host: localhost
        Accept: application/json
        Content-Type: application/json

        {
            "car_id": 1,
            "username": "admin"
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
            "message": {
                "user": ["User is not an admin."]
            }
        }

    :<json string car_id: the id of the car being updated
    :<json string username: the username of the person updating the car
    :>json message: repsonse information such as error information
    :resheader Content-Type: application/json
    :status 200: deletion of car was successful
    :status 401: user is not an admin
    """

    response = {
        'message': '',
    }
    status = 200

    # Checking if user making the request is an admin
    user = User.query.get(request.json["username"])
    if user.role is not Role.admin:
        response['message'] = {
            'user': ['User is not an admin.']
        }
        status = 401
    else:
        car = Car.query.get(request.json["car_id"])
        db.session.delete(car)
        db.session.commit()
        response['message'] = "Success"

    return response, status


@car.route('/cars', methods=["GET"])
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

    if request.args.get('id') is not None:
        id = request.args.get('id')
        car = Car.query.get(id)

        response['cars'] = car_schema.dump(car)
    else:
        cars = None
        if request.args.get('make') is not None:
            make = request.args.get('make')
            cars = Car.query.filter(Car.make.like("%"+make+"%")).all()
        elif request.args.get('body_type') is not None:
            body_type = request.args.get('body_type')
            cars = Car.query.filter(Car.body_type.like("%"+body_type+"%")).all()
        elif request.args.get('colour') is not None:
            colour = request.args.get('colour')
            cars = Car.query.filter(Car.colour.like("%"+colour+"%")).all()
        elif request.args.get('no_seats') is not None:
            no_seats = request.args.get('no_seats')
            cars = Car.query.filter_by(no_seats=no_seats).all()
        elif request.args.get('cost_per_hour') is not None:
            cost_per_hour = request.args.get('cost_per_hour')
            cars = Car.query.filter_by(cost_per_hour=cost_per_hour).all()
        else:
            cars = Car.query.all()
        response['cars'] = car_schema.dump(cars, many=True)

    return response, 200


@car.route('/return', methods=["POST"])
def return_car():
    """Return a car by changing the locked status of a car that has been unlocked

    .. :quickref: Car; Return a car that is booked.

    **Example request**:

    .. sourcecode:: http

        POST /api/return HTTP/1.1
        Host: localhost
        Accept: application/json
        Content-Type: application/json

        {
            "username": "dummy",
            "car_id": 1
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "message": "Car has been returned"
        }

    .. sourcecode:: http

        HTTP/1.1 409 CONFLICT
        Content-Type: application/json

        {
            "message": "ERROR: The car has already been returned"
        }

    :<json string username: the username of the person returning the car
    :<json int car_id: the id of the car being returned
    :>json message: repsonse information such as error information
    :resheader Content-Type: application/json
    :status 200: return was successful
    :status 403: the user is not booked to ride in this car
    :status 409: car is already returned
    """

    response = {
        'message': ''
    }
    status = 200

    username = request.json["username"]
    car_id = request.json["car_id"]
    car = Car.query.get(car_id)

    # Getting the most recent booking for this car
    booking = (Booking.query
               .filter_by(car_id=car_id)
               .order_by(Booking.book_time.desc())
               .first())

    if (booking is not None):
        # Checking if the user requesting to return the car is the last person
        # to ride in it
        if booking.username == username:
            # Checking if already locked
            if car.is_locked:
                response['message'] = "ERROR: The car has already been returned"
                status = 409
            else:
                car.is_locked = True
                db.session.commit()
                response['message'] = "Car has been returned"
        else:
            response['message'] = "ERROR: You have not booked this car"
            status = 403
    else:
        response['message'] = "ERROR: You have not booked this car"
        status = 403

    return response, status


@car.route('/unlock', methods=["POST"])
def unlock_car():
    """Unlock a car by changing the locked status of a car

    .. :quickref: Car; Unlock a car that is booked.

    **Example request**:

    .. sourcecode:: http

        POST /api/return HTTP/1.1
        Host: localhost
        Accept: application/json
        Content-Type: application/json

        {
            "username": "dummy",
            "car_id": 1
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "message": "Car has been unlocked"
        }

    .. sourcecode:: http

        HTTP/1.1 409 CONFLICT
        Content-Type: application/json

        {
            "message": "ERROR: The car is already unlocked"
        }

    :<json string username: the username of the person unlocking the car
    :<json string car_id: the id of the car being unlocked
    :>json message: repsonse information such as error information
    :resheader Content-Type: application/json
    :status 200: unlock was successful
    :status 403: the user is not booked to ride in this car
    :status 409: car is already unlocked
    """

    response = {
        'message': ''
    }
    status = 200

    username = request.json["username"]
    car_id = request.json["car_id"]
    car = Car.query.get(car_id)

    # Getting the most recent booking for this car
    booking = (Booking.query
               .filter_by(car_id=car_id)
               .order_by(Booking.book_time.desc())
               .first())

    if booking is not None:
        # Checking if the user requesting to unlock the car is currently booked
        # to ride in it.
        current_time = datetime.utcnow()
        if (booking.username == username) and (current_time < booking.get_end_time()):
            # Checking if the car is already unlocked
            if car.is_locked:
                car.is_locked = False
                db.session.commit()
                response['message'] = "Car has been unlocked"
            else:
                response['message'] = "ERROR: The car is already unlocked"
                status = 409
        else:
            response['message'] = "ERROR: You have not booked this car"
            status = 403
    else:
        response['message'] = "ERROR: You have not booked this car"
        status = 403

    return response, status


@car.route('/setlocation', methods=["POST"])
def change_car_location():
    """Set a given cars location

    .. :quickref: Car; Change a cars location.

    **Example request**:

    .. sourcecode:: http

        POST /api/setlocation HTTP/1.1
        Host: localhost
        Accept: application/json
        Content-Type: application/json

        {
            "car_id": 1,
            "location": "-37.808880,144.965179"
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "message": "Car location updated"
        }

    :<json string car_id: the id of the car being unlocked
    :<json string location: the latitude and longitude of the new location
    :>json message: response information such as error information
    :resheader Content-Type: application/json
    :status 200: updating location was successful
    :status 404: the car does not exist
    """

    response = {
        'message': ''
    }
    status = 200

    car_id = request.json["car_id"]
    location = request.json["location"]
    car = Car.query.get(car_id)

    # Check location is valid
    if car is not None:
        car.location = location
        db.session.commit()
        response['message'] = "Car location updated"
    else:
        response['message'] = "ERROR: Car does not exist"
        status = 404

    return response, status
