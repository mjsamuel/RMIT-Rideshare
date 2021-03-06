import os

import click, configparser
from flask import Flask

from app.extensions import db, ma, bcrypt
from app.blueprints.api_user import user
from app.blueprints.api_car import car
from app.blueprints.api_booking import booking
from app.blueprints.api_issue import issue
from app.blueprints.site import site
from app.blueprints.docs import docs

def create_app(test_config = None):
    app = Flask(__name__)

    # Loading config.ini file
    user_config = configparser.ConfigParser()
    user_config.read(os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        os.pardir,
        'config.ini'))

    # Checking if in test environment to change config values
    if test_config is None:
        config_state = "DEFAULT"
    else:
        config_state = "TEST"

    # Allows reloading of HTML templates without having to restart application
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # Setting up database connection
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{}:{}@{}/{}".format(
        user_config[config_state]['USER'],
        user_config[config_state]['PASSWORD'],
        user_config[config_state]['HOST'],
        user_config[config_state]['DATABASE'])
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)

    # Creating databse tables
    with app.app_context():
        db.create_all()
        db.session.commit()

    # Registering blueprints
    app.register_blueprint(user)
    app.register_blueprint(car)
    app.register_blueprint(booking)
    app.register_blueprint(issue)
    app.register_blueprint(site)
    app.register_blueprint(docs)

    @app.cli.command("init-db")
    def init_db():
        print("Initializing databse...")
        sql_data_path = os.path.join(
            os.path.dirname(__file__),
            os.pardir, 'tests',
            'data.sql')
        with open(sql_data_path, 'rb') as file:
            sql_commands = file.read().decode('utf8')
        db.session.execute(sql_commands)
        db.session.commit()
        print("Done!")

    @app.cli.command("clear-db")
    def init_db():
        print("Clearing databse...")
        db.drop_all()
        print("Done!")

    return app

def get_db():
    return db
