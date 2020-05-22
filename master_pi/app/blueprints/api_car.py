from flask import Blueprint, request

from app.extensions import db
from app.models.car import Car, car_schema

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

    :<json string car_id: the id of the car being returned
    :>json message: repsonse information such as error information
    :resheader Content-Type: application/json
    :status 200: return was successful
    :status 409: car is already returned
    """

    response = {
        'message': ''
    }
    status = 200

    # Getting car from database
    car_id = request.json["car_id"]
    car = Car.query.get(car_id)

    if car is None:
        print("Car doesnt exist with id '" + car_id + "'")

    # Checking if already locked
    if car.is_locked:
        response['message'] = "ERROR: The car has already been returned"
        status = 409
    else:
        car.is_locked = True
        db.session.commit()
        response['message'] = "Car has been returned"

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

    :<json string car_id: the id of the car being unlocked
    :>json message: repsonse information such as error information
    :resheader Content-Type: application/json
    :status 200: unlock was successful
    :status 409: car is already unlocked
    """

    response = {
        'message': ''
    }
    status = 200

    car_id = request.json["car_id"]
    car = Car.query.get(car_id)

    if car is None:
        print("Car doesnt exist with id '" + car_id + "'")

    if car.is_locked:
        car.is_locked = False
        db.session.commit()
        response['message'] = "Car has been unlocked"
    else:
        response['message'] = "ERROR: The car is already unlocked"
        status = 409

    return response, status
