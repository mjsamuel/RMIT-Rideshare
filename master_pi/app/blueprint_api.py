from flask import Blueprint, current_app, jsonify, request

from app.extensions import db, ma, bcrypt
from app.user import User, user_schema

api = Blueprint("api", __name__, url_prefix='/api')

@api.route('/login', methods = ["POST"])
def login():
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
            password_matche = bcrypt.check_password_hash(user.password, password)
            if password_matche:
                response['message'] = "Logged in successfully "
                response['user'] = user_schema.dump(user)
                status = 200
            else:
                response['message'] = "Incorrect password"
                status = 401

    return response, status

@api.route('/user', methods=["POST"])
def register_user():
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
            if User.query.get(username) is not None:
                response['message'] = "User already exists"
                status = 400
            else:
                # Hashing password
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
    response = {'message': ''}
    status = None

    username = request.args.get('username')
    user = User.query.get(username)
    if user is None:
        response['message'] = "User not found"
        status = 404
    else:
        response = user_schema.dump(user)
        status = 200

    return response, status

@api.route('/user', methods=["DELETE"])
def delete_user():
    username = request.args.get('username')
    return 'Unimplemented'
