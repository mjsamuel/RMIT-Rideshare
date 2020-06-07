from datetime import datetime, timedelta
from flask import Blueprint, request

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from app.extensions import db
from app.models.user import User, user_schema
from app.models.car import Car, car_schema
from app.models.booking import Booking, booking_schema
from app.forms import BookCarFormSchema

booking = Blueprint("booking", __name__, url_prefix='/api')

@booking.route('/booking', methods=['GET'])
def get_bookings():
    """Get a collection of bookings a user has made or for a specific car

    .. :quickref: Booking; Get bookings for a user or car.

    **Example request**:

    .. sourcecode:: http

        GET /api/booking?username=dummy HTTP/1.1
        Host: localhost
        Accept: application/json

    .. sourcecode:: http

        GET /api/booking?car_id=1 HTTP/1.1
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

    :>json bookings: an array of bookings
    :query username: the username to filter by for bookings
    :resheader Content-Type: application/json
    :status 200: bookings found
    """
    response = {
        'bookings': None
    }

    username = request.args.get('username')
    car_id = request.args.get('car_id')
    if username is not None:
        # Getting bookings ordered from most recent, to least recent
        bookings = (Booking.query
            .filter_by(username=username)
            .order_by(Booking.book_time.desc())
            .all())

        # Adding the the car associated with the bookings to be searlized along
        # with them
        for booking in bookings:
            booking.car = Car.query.get(booking.car_id)

        response['bookings'] = booking_schema.dump(bookings, many=True)
    elif car_id is not None:
        # Getting bookings ordered from most recent, to least recent
        bookings = (Booking.query
            .filter_by(car_id=str(car_id))
            .order_by(Booking.book_time.desc())
            .all())

        response['bookings'] = booking_schema.dump(bookings, many=True)

    return response, 200

@booking.route('/booking', methods=['POST'])
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
    status = 200

    form_schema = BookCarFormSchema()
    form_errors = form_schema.validate(request.json)
    if form_errors:
        response['message'] = form_errors
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
            # Checking if the time being booked is after the previous booking's
            # end time
            if (book_time < prev_booking.get_end_time()):
                currently_booked = True
                response['message'] = {
                    'user': ['Car is currently booked.']
                }
                status = 401

        if not currently_booked:
            # Adding to Google calendar if authorised
            gcal_id = None
            user = User.query.get(username)
            if (user.google_credentials is not None):
                car = Car.query.get(car_id)
                service = build('calendar', 'v3', credentials=user.google_credentials)
                end_time = book_time + timedelta(hours=int(duration))
                event = {
                  'summary': 'Ride in {} {}'.format(car.make, car.body_type),
                  'description': 'Booked from RMIT Rideshare app',
                  'start': {
                    'dateTime': str(book_time.isoformat()),
                    'timeZone': 'UTC',
                  },
                  'end': {
                    'dateTime': str(end_time.isoformat()),
                    'timeZone': 'UTC',
                  }
                }
                event = service.events().insert(calendarId='primary', body=event).execute()
                gcal_id = event.get('id')

            # Adding booking to database with Google calendar id if present
            booking = Booking(car_id, username, book_time, duration, gcal_id)
            db.session.add(booking)
            db.session.commit()
            response['message'] = "Success"

    return response, status

@booking.route('/booking', methods=['DELETE'])
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

        {
            'message': 'Deleted successfully'
        }

    :query id: the id of the booking to be deleted
    :>json message: repsonse information such as error information
    :status 200: booking deleted
    """

    response = {
        'message': 'Deleted successfully'
    }
    id = request.args.get('id')
    booking = Booking.query.get(id)

    # Removing from Google calendar if event was created there
    if (booking.gcal_id is not None):
        user = User.query.get(booking.username)
        service = build('calendar', 'v3', credentials=user.google_credentials)
        service.events().delete(calendarId='primary', eventId=booking.gcal_id).execute()

    db.session.delete(booking)
    db.session.commit()

    return response, 200
