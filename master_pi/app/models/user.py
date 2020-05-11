from marshmallow import fields, validates_schema, ValidationError

from app.extensions import db, ma

class User(db.Model):
    """Class to represent a basic user that can hire vehicles

    :param username: The user's unique name to be identfied with and to log in
    :type username: string
    :param password: Hashed password for user to log in with
    :type password: string
    :param f_name: The user's first name
    :type f_name: string
    :param l_name: The user's last name
    :type l_name: string
    :param email: The user's email
    :type email: string
    :param google_credentials: Google authentication information
    :type username: credentials
    """
    username = db.Column(db.String(32), primary_key=True)
    password = db.Column(db.String(128), unique=False, nullable=False)
    f_name = db.Column(db.String(32), unique=False, nullable=False)
    l_name = db.Column(db.String(32), unique=False, nullable=False)
    email = db.Column(db.String(64), unique=False, nullable=False)
    google_credentials = db.Column(db.PickleType(), unique=False, nullable=True)

    def __init__(self, username, password, f_name, l_name, email):
        """Constructor method
        """
        self.username = username
        self.password = password
        self.f_name = f_name
        self.l_name = l_name
        self.email = email

class UserSchema(ma.SQLAlchemySchema):
    """A class to represent the schema for users
    """
    class Meta:
        model = User

    username = fields.Str()

user_schema = UserSchema()
