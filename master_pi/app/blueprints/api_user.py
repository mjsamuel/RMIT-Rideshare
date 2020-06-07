from flask import Blueprint, request
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from app.extensions import db, bcrypt
from app.models.user import User, user_schema
from app.models.booking import Booking, booking_schema
from app.forms import LoginFormSchema, RegisterFormSchema, AuthenticationFormSchema


user = Blueprint("user", __name__, url_prefix='/api')


@user.route('/login', methods = ["POST"])
def login():
    """Endpoint for a user's credentials to be checked in order to log in to their account

    .. :quickref: User; Validate user credentials for login.

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
    :>json app.models.user.User user: the user object that has been created
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
    status = 200

    form_schema = LoginFormSchema()
    form_errors = form_schema.validate(request.json)
    if form_errors:
        response['message'] = form_errors
        status = 400
    else:
        username = request.json["username"]
        password = request.json["password"]

        # Checking if user is in database
        user = User.query.get(username)
        if user is None:
            response['message'] = {
                'user': ['User does not exist.']
            }
            status = 404
        else:
            # Checking wether passwords match
            passwords_match = bcrypt.check_password_hash(user.password, password)
            if passwords_match:
                response['message'] = "Logged in successfully"
                response['user'] = user_schema.dump(user)
                status = 200
            else:
                response['message'] = {
                    'user': ['Incorrect password.']
                }
                status = 401

    return response, status


@user.route('/login_bluetooth', methods = ["POST"])
def login_bluetooth():
    """Endpoint for a user's credentials to be checked in order to log in to their account

    .. :quickref: User; Validate user credentials for login.

    **Example request**:

    .. sourcecode:: http

        POST /api/login_bluetooth HTTP/1.1
        Host: localhost
        Accept: application/json
        Content-Type: application/json

        {
            "username": "dummy",
            "mac_address": "18:F1:D8:E2:E9:6B"
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
            "message": "MAC Address either not set, or does not match received.",
            "user": null
        }

    :<json string username: unique username
    :<json string mac_address: mac address for specified account
    :>json message: repsonse information such as error information
    :>json app.models.user.User user: the user object that has been created
    :resheader Content-Type: application/json
    :status 200: successful login
    :status 401: invalid mac address
    :status 404: user does not exist
    """

    response = {
        'message': '',
        'user': None
    }
    status = 200


    username = request.json["username"]
    mac_address = request.json["mac_address"]

    # Checking if user is in database & find mac address
    user = User.query.get(username)

    if user is None:
        response['message'] = {
            'user': ['User does not exist.']
        }
        status = 404
    else:
        # Grab mac address of user
        mac_address_api = user.mac_address
        # Checking whether mac_address given matches username
        if mac_address_api == mac_address:
            response['message'] = "Logged in successfully"
            response['user'] = user_schema.dump(user)
            status = 200
        else:
            response['message'] = {
                'user': ['MAC Address either not set, or does not match received.']
            }
            status = 401

    return response, status


@user.route('/user', methods=["POST"])
def register_user():
    """Creates a user account that does not already exist

    .. :quickref: User; Create new user.

    **Example request**:

    .. sourcecode:: http

        POST /api/user HTTP/1.1
        Host: localhost
        Accept: application/json
        Content-Type: application/json

        {
            "username": "dummy",
            "f_name": "John",
            "l_name": "Doe",
            "email": "test@gmail.com",
            "password": "abcd",
            "confirm_password": "abcd"
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
    :<json string f_name: first name of the user
    :<json string l_name: last name of the user
    :<json string email: email of the user (in the correct format)
    :<json string password: password for new accoutn
    :<json string confirm_password: retyped password which should match the previous password value
    :>json message: repsonse information such as error information
    :>json app.models.user.User user: the user object that has been created
    :resheader Content-Type: application/json
    :status 200: successful registration
    :status 400: malformed request
    """

    response = {
        'message': '',
        'user': None
    }
    status = 200

    # Checking that form data is correct
    form_schema = RegisterFormSchema()
    form_errors = form_schema.validate(request.json)
    if form_errors:
        response['message'] = form_errors
        status = 400
    else:
        username = request.json["username"]
        f_name =  request.json["f_name"]
        l_name =  request.json["l_name"]
        email =  request.json["email"]
        password = request.json["password"]
        confirm_password = request.json["confirm_password"]

        # Checking that user is not already in the system
        if User.query.get(username) is not None:
            response['message'] = {
                'user': ['User already exists.']
            }
            status = 400
        else:
            # Hashing password using brcypt's one-way encryption
            hashed_password = bcrypt.generate_password_hash(password)

            # Creating user and adding to the database
            new_user = User(username, hashed_password, f_name, l_name, email)
            db.session.add(new_user)
            db.session.commit()

            response['message'] = "Registered user successfully"
            response['user'] = user_schema.dump(new_user)

    return response, status


@user.route('/register_bluetooth', methods=["POST"])
def register_bluetooth():
    """Updates a users bluetooth mac address identifier

    .. :quickref: User Bluetooth; Update users Bluetooth.

    **Example request**:

    .. sourcecode:: http

        POST /api/register_bluetooth HTTP/1.1
        Host: localhost
        Accept: application/json
        Content-Type: application/json

        {
            "username": "dummy",
            "mac_address": "18:F1:D8:E2:E9:6B"
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "message": "User MAC Address updated",
            "user": {
                "username": "dummy"
            }
        }

    .. sourcecode:: http

        HTTP/1.1 404 BAD REQUEST
        Content-Type: application/json

        {
            "message": "ERROR: User does not exist",
        }

    :<json string username: username that exists within the database
    :<json string mac_address: mac address of users bluetooth device
    :>json message: repsonse information such as error information
    :>json app.models.user.User loggedin_user: the user object that is logged in
    :resheader Content-Type: application/json
    :status 200: successful registration
    :status 404: invalid user
    """

    response = {
        'message': ''
    }
    status = 200

    username = request.json["username"]
    mac_address = request.json["mac_address"]
    loggedin_user = User.query.get(username)

    if loggedin_user is not None:
        loggedin_user.mac_address = mac_address
        db.session.commit()
        response['message'] = "User MAC Address updated"
    else:
        response['message'] = "ERROR: User does not exist"
        status = 404

    return response, status


@user.route('/user', methods=["GET"])
def get_user():
    """Gets a user from the database

    .. :quickref: User; Get a user.

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

    :query username: the username that you are searching for
    :>json message: repsonse information such as error information
    :>json app.models.user.User user: the user object found
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


@user.route('/googleauth', methods=['GET'])
def get_auth_link():
    """Retirieves a url to link a user's google account to this application

    .. :quickref: Google Auth; Get an authentication link.

    **Example request**:

    .. sourcecode:: http

        GET /api/googleauth HTTP/1.1
        Host: localhost
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK

        {
            "auth_url": "..."
        }

    :status 200: succesfully sent url
    """

    response = {
        'auth_url': None
    }

    # Creating flow for user authentication for calendar read/write access
    flow = Flow.from_client_secrets_file(
        '../credentials.json',
        ['https://www.googleapis.com/auth/calendar'],
        redirect_uri='urn:ietf:wg:oauth:2.0:oob')

    auth_url, _ = flow.authorization_url(prompt='consent')
    response['auth_url'] = auth_url

    return response, 200


@user.route('/googleauth', methods=['POST'])
def add_auth_credentials():
    """Add Google credentials to a user to access Google Calendar

    .. :quickref: Google Auth; Link Google account to user account.

    **Example request**:

    .. sourcecode:: http

        POST /api/googleauth HTTP/1.1
        Host: localhost
        Accept: application/json
        Content-Type: application/json

        {
            "username": "dummy",
            "code": "4/zgHpKQ9ASBXjkOTgjVucu_8GJAVrqQt5veJfXhzAcd6iWjyAI3a21xI"
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "message": "Success"
        }

    :<json string username: username that will be linked to the Google account
    :<json string code: authenticaiton code to allow link
    :>json message: repsonse information such as error information
    :status 200: succesfully added credentials
    :status 400: malformed request
    :status 500: server error
    """

    response = {
        'message': None
    }
    status = None

    form_schema = AuthenticationFormSchema()
    form_errors = form_schema.validate(request.json)
    if form_errors:
        response['message'] = form_errors
        status = 400
    else:
        username = request.json["username"]
        code = request.json["code"]

        flow = Flow.from_client_secrets_file(
            '../credentials.json',
            ['https://www.googleapis.com/auth/calendar'],
            redirect_uri='urn:ietf:wg:oauth:2.0:oob')
        try:
            flow.fetch_token(code=code)
            credentials = flow.credentials
            # Updating user in database with credentials
            user = User.query.get(username)
            user.google_credentials = credentials
            db.session.commit()
            response['message'] = "Success"
            status = 200
        except:
            response['message'] = {
                'error': ['Google authentication error occured.']
            }
            status = 500

    return response, status
