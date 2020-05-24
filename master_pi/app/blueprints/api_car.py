from flask import Blueprint, request
from datetime import datetime

from app.extensions import db
from app.models.car import Car, car_schema
from app.models.booking import Booking

car = Blueprint("car", __name__, url_prefix='/api')


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
    status = None

    if request.args.get('id') is not None:
        id = request.args.get('id')
        car = Car.query.get(id)

        response['cars'] = car_schema.dump(car)
        status = 200
    else:
        cars = None
        if request.args.get('make') is not None:
            make = request.args.get('make')
            cars = Car.query.filter_by(make=make).all()
        elif request.args.get('body_type') is not None:
            body_type = request.args.get('body_type')
            cars = Car.query.filter_by(body_type=body_type).all()
        elif request.args.get('colour') is not None:
            colour = request.args.get('colour')
            cars = Car.query.filter_by(colour=colour).all()
        elif request.args.get('no_seats') is not None:
            no_seats = request.args.get('no_seats')
            cars = Car.query.filter_by(no_seats=no_seats).all()
        elif request.args.get('cost_per_hour') is not None:
            cost_per_hour = request.args.get('cost_per_hour')
            cars = Car.query.filter_by(cost_per_hour=cost_per_hour).all()
        else:
            cars = Car.query.all()
        response['cars'] = car_schema.dump(cars, many=True)
        status = 200

    return response, status


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
            "car_id": 1,
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
    :<json string car_id: the id of the car being returned
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
            "car_id": 1,
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

        POST /api/return HTTP/1.1
        Host: localhost
        Accept: application/json
        Content-Type: application/json

        {
            "car_id": 1,
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "message": "Car location updated"
        }

    .. sourcecode:: http

        HTTP/1.1 403 CONFLICT
        Content-Type: application/json

        {
            "message": "ERROR: Car location not updated. Location given error."
        }

    :<json string car_id: the id of the car being unlocked
    :<json string location: the latitude and longitude of the new location
    :>json message: response information such as error information
    :resheader Content-Type: application/json
    :status 200: update was successful
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
