from flask import Blueprint, render_template, request
import requests, json
from app.extensions import ma

site = Blueprint("site", __name__,
    template_folder='templates',
    static_folder='static')


@site.route('/login')
def login():
    return render_template('login.html', title='Login')


@site.route('/register')
def register():
    return render_template('shared/edit_user.html', title='Register', user=None)


@site.route('/')
def booked_cars():
    return render_template('default/user_console.html', title='Booked Cars')


@site.route('/cars')
def search_cars():
    return render_template('shared/list_cars.html', title='Cars')


@site.route('/car')
def book_car():
    car_id = request.args.get('id')
    response = requests.get('http://localhost:5000/api/cars?id=' + car_id)
    data = json.loads(response.text)
    title = data['cars']['make'] + ' - ' + data['cars']['body_type']

    return render_template('default/book_car.html', title=title, car=data['cars'])


@site.route('/google-account')
def link_google_account():
    return render_template('default/link_google_account.html', title='Link Your Google Account')


# Admin specific routes
@site.route('/admin-console')
def admin_console():
    return render_template('admin/admin_console.html', title='Admin Console')


@site.route('/manage-users')
def manage_user():
    return render_template('admin/search_users.html', title='Manage Users')


@site.route('/new-user')
def new_user():
    return render_template('shared/edit_user.html', title='New User', user=None)


@site.route('/edit-user')
def edit_user():
    username = request.args.get('username')
    response = requests.get('http://localhost:5000/api/user?username=' + username)
    data = json.loads(response.text)
    return render_template('shared/edit_user.html', title='Edit User', user=data['users'])


@site.route('/manage-cars')
def manage_cars():
    return render_template('shared/list_cars.html', title='Manage Cars', admin=True)


@site.route('/new-car')
def new_car():
    return render_template('admin/edit_car.html', title="New Car", car=None)


@site.route('/edit-car')
def edit_car():
    car_id = request.args.get('id')
    response = requests.get('http://localhost:5000/api/cars?id=' + car_id)
    data = json.loads(response.text)

    return render_template('admin/edit_car.html', title="Edit Car", car=data['cars'])


@site.route('/report-issue')
def report_issue():
    car_id = request.args.get('id')
    response = requests.get('http://localhost:5000/api/cars?id=' + car_id)
    data = json.loads(response.text)

    return render_template('admin/report_issue.html', title="Report Issue", car=data['cars'])


# Engineer specific routes
@site.route('/engineer-console')
def engineer_console():
    return render_template('engineer/engineer_console.html', title='Engineer Console')


@site.route('/issue')
def issue():
    issue_id = request.args.get('id')
    response = requests.get('http://localhost:5000/api/issue?id=' + issue_id)
    data = json.loads(response.text)
    title = "Issue - #" + str(data['issues']['id'])

    return render_template('engineer/issue.html', title=title, issue=data['issues'])


@site.route('/pushbullet-account')
def link_pushbullet_account():
    return render_template('engineer/link_pushbullet_account.html', title='Link Your Pushbullet Account')


# Manager specific routes
@site.route('/manager-console')
def manager_console():
    return render_template('shared/list_cars.html', title='Manager Console', manager=True)


@site.route('/statistics-car')
def statistics_car():
    car_id = request.args.get('id')
    response = requests.get('http://localhost:5000/api/cars?id=' + car_id)
    data = json.loads(response.text)

    return render_template('manager/statistics_car.html', title="Car Statistics", car=data['cars'])
