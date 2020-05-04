import os

import configparser
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from app.blueprint_api import api
from app.blueprint_site import site


# Reading from config.ini file
config = configparser.ConfigParser()
config.read(os.path.join(
    os.path.dirname(__file__),
    os.pardir,
    os.pardir,
    'config.ini'))

# Setting up Flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{}:{}@{}/{}".format(
    config['DEFAULT']['USER'],
    config['DEFAULT']['PASSWORD'],
    config['DEFAULT']['HOST'],
    config['DEFAULT']['DATABASE'])

db = SQLAlchemy(app)
ma = Marshmallow(app)

app.register_blueprint(api)
app.register_blueprint(site)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
