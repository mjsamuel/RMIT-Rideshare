from app.extensions import db, ma
from marshmallow import fields

class User(db.Model):
    """Class to represent a basic user that can hire vehicles

    :param username: The user's unique name to be identfied with and to log in
    :type username: string
    :param password: Hashed password for user to log in with
    :type password: string
    """
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(128), unique=False, nullable=False)

    def __init__(self, username, password):
        """Constructor method
        """
        self.username = username
        self.password = password

class UserSchema(ma.SQLAlchemySchema):
    """A class to represent the schema for users
    """
    class Meta:
        model = User

    username = fields.Str()

user_schema = UserSchema()
