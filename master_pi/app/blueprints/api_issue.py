from flask import Blueprint, request
from datetime import datetime

from app.extensions import db
from app.models.user import User, Role
from app.models.car import Car
from app.models.issue import Issue
from app.forms import ReportIssueFormSchema

issue = Blueprint("issue", __name__, url_prefix='/api')

@issue.route('/issue', methods=["POST"])
def new_issue():
    """Report an issue with a car if the user making the report is an admin

    .. :quickref: Issue; Report a new issue.

    **Example request**:

    .. sourcecode:: http

        POST /api/car HTTP/1.1
        Host: localhost
        Accept: application/json
        Content-Type: application/json

        {
            "car_id": 1,
            "username": "admin",
            "details": "Broken tail light"
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "message": "Success"
        }

    .. sourcecode:: http

        HTTP/1.1 401 UNAUTHORIZED
        Content-Type: application/json

        {
            "message": {
                "user": ["User is not an admin."]
            }
        }

    :<json int car_id: the make of the car being updated
    :<json string username: the username of the person reporting the issue
    :<json string details: details of what the issue may be
    :resheader Content-Type: application/json
    :status 200: creating a new car was successful
    :status 400: missing or invalid fields
    :status 401: user is not an admin
    """

    response = {
        'message': '',
    }
    status = 200

    form_schema = ReportIssueFormSchema()
    form_errors = form_schema.validate(request.json)
    if form_errors:
        response['message'] = form_errors
        status = 400
    else:
        # Checking if user making the request is an admin
        user = User.query.get(request.json["username"])
        if user.role is not Role.admin:
            response['message'] = {
                'user': ['User is not an admin.']
            }
            status = 401
        else:
            car_id = request.json["car_id"]
            time = datetime.utcnow()
            details = request.json["details"]

            issue = Issue(car_id, time, details)
            db.session.add(issue)
            db.session.commit()
            response['message'] = "Success"

    return response, status
