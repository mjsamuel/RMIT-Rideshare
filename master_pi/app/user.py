from app.database import db, ma

class User(db.Model):
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(128), unique=False, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    username = ma.auto_field()

user_schema = UserSchema()
