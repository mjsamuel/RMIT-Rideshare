from app.extensions import db, ma
from marshmallow import fields

class Car(db.Model):
    """Class to represent a car that can be hired by a user

    :param id: unique id of the car to be stored in the database
    :type id: int
    :param make: the manufacturer of the car
    :type make: string
    :param body_type: the type of shape of the car (e.g. sedan, hatchback, SUV)
    :type body_type: string
    :param colour: the colour of the car
    :type colour: string
    :param no_seats: number of seats of the car
    :type no_seats: int
    :param location: the current location of the car
    :type location: string
    :param cost_per_hour: the cost per hour to hire the car
    :type cost_per_hour: int
    :param is_locked: indicates if the car is currently locked
    :type is_locked: boolean
    """

    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(128), unique=False, nullable=False)
    body_type = db.Column(db.String(128), unique=False, nullable=False)
    colour = db.Column(db.String(128), unique=False, nullable=False)
    no_seats = db.Column(db.Integer, unique=False, nullable=False)
    location = db.Column(db.String(128), unique=False, nullable=True)
    cost_per_hour = db.Column(db.Integer, unique=False, nullable=False)
    is_locked = db.Column(db.Boolean, unique=False, nullable=False)

    def __init__(self, make, body_type, colour, no_seats, cost_per_hour, is_locked):
        """Constructor method
        """
        self.make = make
        self.body_type = body_type
        self.colour = colour
        self.no_seats = no_seats
        self.cost_per_hour = cost_per_hour
        self.is_locked = is_locked

class CarSchema(ma.SQLAlchemySchema):
    """A class to represent the schema for cars
    """
    class Meta:
        model = Car

    id = fields.Int()
    make = fields.Str()
    body_type = fields.Str()
    colour = fields.Str()
    no_seats = fields.Int()
    location = fields.Str()
    cost_per_hour = fields.Int()
    is_booked = fields.Boolean()
    is_locked = fields.Boolean()

car_schema = CarSchema()
