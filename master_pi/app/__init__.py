import os

import configparser
from flask import Flask

from app.database import db, ma
from app.blueprint_api import api
from app.blueprint_site import site

# Reading from config.ini file
config = configparser.ConfigParser()
config.read(os.path.join(
    os.path.dirname(__file__),
    os.pardir,
    os.pardir,
    'config.ini'))

app = Flask(__name__)

# Reloads HTML templates without having to restart application
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Setting up database connection
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{}:{}@{}/{}".format(
    config['DEFAULT']['USER'],
    config['DEFAULT']['PASSWORD'],
    config['DEFAULT']['HOST'],
    config['DEFAULT']['DATABASE'])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db.init_app(app)
ma.init_app(app)

# Creating databse tables
with app.app_context():
    db.create_all()
    db.session.commit()

# Registering blueprints
app.register_blueprint(api)
app.register_blueprint(site)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
