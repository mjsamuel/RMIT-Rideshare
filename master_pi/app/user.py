from app import db
from app import ma

class User(db.Model):
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(64), unique=False, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserSchema(ma.ma.SQLAlchemySchema):
    class Meta:
        model = User

    username = ma.auto_field()
    password = ma.auto_field()
