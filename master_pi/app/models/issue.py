from marshmallow import fields

from app.extensions import db, ma
from app.models.car import CarSchema

class Issue(db.Model):
    """Class to represent an issue for a car

    :param id: unique id of the issue
    :type id: int
    :param car_id: the id of the car that has the issue
    :type car_id: int
    :param time: the time (in utc format) that the issue was reported
    :type time: datetime
    :param details: details of the car's issue
    :type details: string
    :param car: variable to easily serialize issue along with a car object (not stored in database), optional
    :type car: app.model.car.Car
    """

    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, unique=False, nullable=False)
    time = db.Column(db.DateTime, unique=False, nullable=False)
    details = db.Column(db.String(128), unique=False, nullable=True)
    car = None

    def __init__(self, car_id, time, details):
        """Constructor method
        """
        self.car_id = car_id
        self.time = time
        self.details = details

class IssueSchema(ma.SQLAlchemySchema):
    """A class to represent the schema for a issue
    """
    class Meta:
        model = Issue

    id = fields.Int()
    car_id = fields.Int()
    time = fields.DateTime()
    details = fields.Str()
    car = fields.Nested(CarSchema)

issue_schema = IssueSchema()
