from marshmallow import fields, Schema, ValidationError, validates, validates_schema
import re

from app.models.user import User

class LoginFormSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

    @validates('username')
    def username_empty(self, value):
        if value == "":
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
        if value == "":
            raise ValidationError("Missing username.")

    @validates('f_name')
    def f_name_empty(self,value):
        if value == "":
            raise ValidationError("Missing first name.")

    @validates('l_name')
    def l_name_empty(self, value):
        if value == "":
            raise ValidationError("Missing username.")

    @validates('password')
    def password_empty(self, value):
        if value == "":
            raise ValidationError("Missing password.")

    @validates('confirm_password')
    def conf_password_empty(self, value):
        if value == "":
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
        if value == "":
            raise ValidationError("Missing username.")

    @validates('code')
    def username_empty(self, value):
        if value == "":
            raise ValidationError("Missing code.")


class PushbulletFormSchema(Schema):
    username = fields.Str(required=True)
    token = fields.Str(required=True)

    @validates('username')
    def username_empty(self, value):
        if value == "":
            raise ValidationError("Missing username.")

    @validates('token')
    def username_empty(self, value):
        if value == "":
            raise ValidationError("Missing token.")


class BookCarFormSchema(Schema):
    car_id = fields.Int(required=True)
    username = fields.Str(required=True)
    duration = fields.Int(required=True)

    @validates('duration')
    def username_empty(self, value):
        if value < 1:
            raise ValidationError("Duration must be a positive integer.")


class EditCarFormSchema(Schema):
    car_id = fields.Int(required=False)
    username = fields.Str(required=True)
    make = fields.Str(required=True)
    body_type = fields.Str(required=True)
    colour = fields.Str(required=True)
    no_seats = fields.Int(required=True)
    location = fields.Str(required=True)
    cost_per_hour = fields.Int(required=True)

    @validates('make')
    def validate_make(self, value):
        if value == "":
            raise ValidationError("Missing make.")

    @validates('body_type')
    def validate_body_type(self, value):
        if value == "":
            raise ValidationError("Missing body type.")

    @validates('colour')
    def username_empty(self, value):
        if value == "":
            raise ValidationError("Missing colour.")

    @validates('no_seats')
    def validate_no_seats(self, value):
        if value == "":
            raise ValidationError("Missing number of seats.")
        if value < 1:
            raise ValidationError("Number of seats must be a positive integer.")

    @validates('location')
    def validate_location(self, value):
        if value == "":
            raise ValidationError("Missing location.")

        valid_location = re.search("^(-?\d+(\.\d+)?),*(-?\d+(\.\d+)?)$", value)
        if not valid_location:
            raise ValidationError("Location is not a valid latitude/longitude.")

    @validates('cost_per_hour')
    def validate_cost_per_hour(self, value):
        if value == "":
            raise ValidationError("Missing cost per hour.")
        if value < 1:
            raise ValidationError("Cost per hour must be a positive integer.")


class ReportIssueFormSchema(Schema):
    car_id = fields.Int(required=False)
    username = fields.Str(required=True)
    details = fields.Str(required=True)

    @validates('details')
    def validate_details(self, value):
        if value == "":
            raise ValidationError("Missing details.")
