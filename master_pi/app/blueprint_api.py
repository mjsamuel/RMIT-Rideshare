from flask import Blueprint, current_app, jsonify, request

from app.extensions import db, ma, bcrypt
from app.user import User, user_schema

api = Blueprint("api", __name__, url_prefix='/api')

@api.route('/login', methods = ["POST"])
def login():
    """Endpoint for a user's credentials to be checked in order to log in to their account

    .. :quickref: POST; Validate user credentials for login.

    **Example request**:

    .. sourcecode:: http

        POST /api/login HTTP/1.1
        Host: localhost
        Accept: application/json
        Content-Type: application/json

        {
            "username": "dummy",
            "password": "abcd"
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "message": "Logged in successfully",
            "user": {
                "username": "dummy"
            }
        }

    .. sourcecode:: http

        HTTP/1.1 401 UNAUTHORIZED
        Content-Type: application/json

        {
            "message": "Incorrect password",
            "user": null
        }

    :<json string username: unique username
    :<json string password: password for specified account
    :>json message: repsonse information such as error information
    :>json app.user.User user: the user object that has been created
    :resheader Content-Type: application/json
    :status 200: successful login
    :status 400: malformed request
    :status 401: incorrect password
    :status 404: user does not exist
    """
    response = {
        'message': '',
        'user': None
    }
    status = None

    if ('username' not in request.json) or (request.json["username"] == ""):
        response['message'] = "Missing username"
        status = 400
    elif ('password' not in request.json) or (request.json["password"] == ""):
        response['message'] = "Missing password"
        status = 400
    else:
        username = request.json["username"]
        password = request.json["password"]

        user = User.query.get(username)
        if user is None:
            response['message'] = "User does not exist"
            status = 404
        else:
            password_match = bcrypt.check_password_hash(user.password, password)
            if password_match:
                response['message'] = "Logged in successfully"
                response['user'] = user_schema.dump(user)
                status = 200
            else:
                response['message'] = "Incorrect password"
                status = 401

    return response, status

@api.route('/user', methods=["POST"])
def register_user():
    """Creates a user account that does not already exist

    .. :quickref: POST; Create new user.

    **Example request**:

    .. sourcecode:: http

        POST /api/user HTTP/1.1
        Host: localhost
        Accept: application/json
        Content-Type: application/json

        {
            "username": "dummy",
            "password": "abcd",
            "confirm-password": "abcd"
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "message": "Registered user successfully",
            "user": {
                "username": "dummy"
            }
        }

    .. sourcecode:: http

        HTTP/1.1 400 BAD REQUEST
        Content-Type: application/json

        {
            "message": "Passwords do not match",
            "user": null
        }

    :<json string username: username that does not already exist within the database
    :<json string password: password for new accoutn
    :<json string confirm-password: retyped password which should match the previous password value
    :>json message: repsonse information such as error information
    :>json app.user.User user: the user object that has been created
    :resheader Content-Type: application/json
    :status 200: successful registration
    :status 400: malformed request
    """
    response = {
        'message': '',
        'user': None
    }
    status = None

    if ('username' not in request.json) or (request.json["username"] == ""):
        response['message'] = "Missing username"
        status = 400
    elif ('password' not in request.json) or (request.json["password"] == ""):
        response['message'] = "Missing password"
        status = 400
    elif ('confirm_password' not in request.json) or (request.json["confirm_password"] == ""):
        response['message'] = "Missing confirmed password"
        status = 400
    else:
        username = request.json["username"]
        password = request.json["password"]
        confirm_password = request.json["confirm_password"]

        if password != confirm_password:
            response['message'] = "Passwords do not match"
            status = 400
        else:
            # Querying database to check if user already exists in the system
            if User.query.get(username) is not None:
                response['message'] = "User already exists"
                status = 400
            else:
                # Hashing password using brcypt's one-way encryption
                hashed_password = bcrypt.generate_password_hash(password)

                new_user = User(username, hashed_password)
                db.session.add(new_user)
                db.session.commit()

                response['message'] = "Registered user successfully"
                response['user'] = user_schema.dump(new_user)
                status = 200

    return response, status


@api.route('/user', methods=["GET"])
def get_user():
    """Gets a user from the database

    .. :quickref: GET; Get a user.

    **Example request**:

    .. sourcecode:: http

        GET /api/user?username=dummy HTTP/1.1
        Host: localhost
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "message": "User found",
            "user": {
                "username": "dummy"
            }
        }

    .. sourcecode:: http

        HTTP/1.1 404 NOT FOUND
        Content-Type: application/json

        {
            "message": "User not found",
            "user": null
        }

    :>json message: repsonse information such as error information
    :>json app.user.User user: the user object found
    :resheader Content-Type: application/json
    :status 200: user found
    :status 404: user does not exit
    """
    response = {
        'message': '',
        'user': None
    }
    status = None

    username = request.args.get('username')
    user = User.query.get(username)
    if user is None:
        response['message'] = "User not found"
        status = 404
    else:
        response['message'] = "User found"
        response['user'] = user_schema.dump(user)
        status = 200

    return response, status

@api.route('/user', methods=["DELETE"])
def delete_user():
    username = request.args.get('username')
    return 'Unimplemented'
