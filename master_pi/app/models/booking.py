from app.extensions import db, ma
from marshmallow import fields

class Booking(db.Model):
    """Class to represent a user booking a vehicle

    :param id: unique id of the booking
    :type id: int
    :param carId: the id of the car that has been booked by the user
    :type carId: id
    :param username: username of the person that has booked the car
    :type username: string
    :param date: the date that the car is booked
    :type date: datetime
    """

    id = db.Column(db.Integer, primary_key=True)
    carId = db.Column(db.Integer, unique=False, nullable=False)
    username = db.Column(db.String(128), unique=False, nullable=False)
    date = db.Column(db.DateTime, unique=False, nullable=False)

    def __init__(self, carId, username, date):
        """Constructor method
        """
        self.make = make
        self.carId = carId
        self.username = username
        self.date = date

class BookingSchema(ma.SQLAlchemySchema):
    """A class to represent the schema for a booking
    """
    class Meta:
        model = Booking

    id = fields.Int()
    carId = fields.Int()
    username = fields.Str()
    date = fields.DateTime()

booking_schema = BookingSchema()
