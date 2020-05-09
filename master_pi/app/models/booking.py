from app.extensions import db, ma
from marshmallow import fields

class Booking(db.Model):
    """Class to represent a user booking for a vehicle

    :param id: unique id of the booking
    :type id: int
    :param car_id: the id of the car that has been booked by the user
    :type car_id: id
    :param username: username of the person that has booked the car
    :type username: string
    :param book_time: the time (in utc format) that the car was booked
    :type book_time: datetime
    :param duration: the total time that the car has been booked for
    :type duration: int
    """

    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, unique=False, nullable=False)
    username = db.Column(db.String(128), unique=False, nullable=False)
    book_time = db.Column(db.DateTime, unique=False, nullable=False)
    duration = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, car_id, username, book_time, duration):
        """Constructor method
        """
        self.car_id = car_id
        self.username = username
        self.book_time = book_time
        self.duration = duration

class BookingSchema(ma.SQLAlchemySchema):
    """A class to represent the schema for a booking
    """
    class Meta:
        model = Booking

    id = fields.Int()
    car_id = fields.Int()
    username = fields.Str()
    book_time = fields.DateTime()
    duration = fields.Int()

booking_schema = BookingSchema()
