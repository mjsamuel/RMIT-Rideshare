from marshmallow import fields, Schema, ValidationError, validates, validates_schema
from app.models.user import User

class LoginFormSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

    @validates('username')
    def username_empty(self, value):
        if (value == ""):
            raise ValidationError("Missing username.")

    @validates('password')
    def password_empty(self, value):
        if (value == ""):
            raise ValidationError("Missing password.")

class RegisterFormSchema(Schema):
    username = fields.Str(required=True)
    f_name = fields.Str(required=True)
    l_name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    confirm_password = fields.Str(required=True)

    @validates('username')
    def username_empty(self, value):
        if (value == ""):
            raise ValidationError("Missing username.")

    @validates('f_name')
    def f_name_empty(self,value):
        if (value == ""):
            raise ValidationError("Missing first name.")

    @validates('l_name')
    def l_name_empty(self, value):
        if (value == ""):
            raise ValidationError("Missing username.")

    @validates('password')
    def password_empty(self, value):
        if (value == ""):
            raise ValidationError("Missing password.")

    @validates('confirm_password')
    def conf_password_empty(self, value):
        if (value == ""):
            raise ValidationError("Missing confirmed password.")

    @validates_schema
    def validate_password(self, data, **kwargs):
        if data["password"] != data["confirm_password"]:
            raise ValidationError("Passwords do not match.")

class AuthenticationFormSchema(Schema):
    username = fields.Str(required=True)
    code = fields.Str(required=True)

    @validates('username')
    def username_empty(self, value):
        if (value == ""):
            raise ValidationError("Missing username.")

    @validates('code')
    def username_empty(self, value):
        if (value == ""):
            raise ValidationError("Missing code.")

class BookCarFormSchema(Schema):
    car_id = fields.Int(required=True)
    username = fields.Str(required=True)
    duration = fields.Int(required=True)
