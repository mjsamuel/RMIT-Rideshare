from flask import Blueprint, request
from datetime import datetime
import requests, json

from app.extensions import db
from app.models.user import User, Role
from app.models.car import Car
from app.models.issue import Issue, issue_schema
from app.forms import ReportIssueFormSchema

issue = Blueprint("issue", __name__, url_prefix='/api')

@issue.route('/issue', methods=["POST"])
def new_issue():
    """Report an issue with a car if the user making the report is an admin.
    Also send notifications to all engineers via pushbullet that an issue has
    been reported

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

    if response['message'] == "Success":
        # Notifying every engineer via Pushbullet if they have a token
        engineers = (User.query
            .filter(User.role == Role.engineer)
            .filter(User.pb_token != None)
            .all())
        for engineer in engineers:
            data = {
                "type": "note",
                "title": "Issue with car #" + str(car_id),
                "body": details
            }
            # Making request to pushbullet API
            requests.post(
                'https://api.pushbullet.com/v2/pushes',
                data=json.dumps(data),
                headers= {
                    'Authorization': 'Bearer ' + engineer.pb_token,
                    'Content-Type': 'application/json'
                }
            )

    return response, status


@issue.route('/issue', methods=["GET"])
def get_issues():
    """Get a collection of issues or s specific issue

    .. :quickref: Issue; Get bookings for a user or car.

    **Example request**:

    .. sourcecode:: http

        GET /api/issue?id=1 HTTP/1.1
        Host: localhost
        Accept: application/json

    .. sourcecode:: http

        GET /api/issue HTTP/1.1
        Host: localhost
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "issues": [
                {
                    "id": 4,
                    "car_id": 1,
                    "username": "dummy",
                    "book_time": "2020-05-09T13:38:17",
                    "duration": 2,
                    "car": {
                        "make": "Tesla,",
                        "body_type", "Pickup"
                        "...": "..."
                    }
                }
            ]
        }

    :>json issues: an array of issues
    :query id: the id of the issue
    :resheader Content-Type: application/json
    :status 200: bookings found
    """
    response = {
        'issues': None
    }

    if request.args.get('id') is not None:
        id = request.args.get('id')
        issue = Issue.query.get(id)
        issue.car = Car.query.get(issue.car_id)

        response['issues'] = issue_schema.dump(issue)
    else:
        # Getting all isssues ordered from most recent, to least recent
        issues = (Issue.query
            .order_by(Issue.time.desc())
            .limit(25)
            .all())

        # Adding the the car associated with the issue to be searlized along
        # with them
        for issue in issues:
            issue.car = Car.query.get(issue.car_id)

        response['issues'] = issue_schema.dump(issues, many=True)

    return response, 200
