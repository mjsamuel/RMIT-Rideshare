

<div align="center">
  <h1>
    <img src="/docs/images/rpi_logo.png?raw=true" alt="Raspberry Pi Logo" height="125"><br>
    Programming Internet of Things<br> Assignment 3<br>
    <img src="https://travis-ci.com/mjsamuel/IoT-Assignment3.svg?token=8bnx6syKrM5BbM1FTCfx&branch=master"/><br>
  </h1>
  <strong>Ride Share IoT Application</strong><br>
  <sub>Matthew Samuel, Sakaowduan Artpru, Oskar Floeck and Patrick Jones
  </sub>
</div>

## Table of Contents
- [About](#about)
- [Screenshots](#screenshots)
- [Architecture](#architecture)
- [Dependencies](#dependencies)
- [Usage / Development Setup](#usage--development-setup)
  - [Master Pi](#master-pi)
  - [Agent Pi](#agent-pi)
  - [Compiling Sphinx Documentation](#compiling-sphinx-documentation)

## About
RMIT Rideshare is a stripped down ride sharing service written in Python.

It allows users to view a car's location on a map, book it, and have it added to their Google calendar.

When users reach a car they have booked, a CLI is used to interface with it.
It allows the user to login (using their user credentials, a QR code, a Bluetooth device or a picture of their face), unlock the car, and return it.

There are multiple user roles, including managers that can view the statistics of cars, engineers that can can view issues for cars and receive Pushbullet notifications when an issue occurs, as well as admins that can manage all user and car data.

## Screenshots
| Book Car Page                                         | Booking History Page                                       |
| :-------------------------------------------------:   | :-------------------------------------------------:        |
| ![](/docs/images/screenshots/book_car.png?raw=true)   | ![](/docs/images/screenshots/booking_history.png?raw=true) |
| **Manager Statistics Page**                           | **Edit Car Page**                                          |
| ![](/docs/images/screenshots/statistics.png?raw=true) | ![](/docs/images/screenshots/edit_car.png?raw=true)        |

## Architecture
The project is broken up into two sections, each with their own functionality:
- A **Master Pi** that acts as the central server that all requests are made to
- An **Agent Pi** that represents a single car in the database and communicates with the Master Pi

| Pi            | Functionality                                    |
| :------------ | :----------------------------------------------- |
| **Master Pi** | Hosts the RESTful API                            |
|               | Hosts the frontend website                       |
|               | Runs a TCP socket server                         |
|               | Processes images for facial recognition          |
|               | Runs the Google Assistant for speech recognition |
| **Agent Pi**  | Runs a TCP socket client                         |
|               | Scans and recognises devices via Bluetooth       |
|               | Process images for QR code scanning              |

### Technologies used
- Flask
- MySQL
- TCP sockets
- Bluetooth
- Facial recognition using OpenCV
- QR code scanning using ZBar
- Google Maps API
- Google Calendar API
- Google Assistant SDK
- Google Charts API
- Pushbullet API

## Dependencies
- [Python >= 3.5](https://www.python.org)

## Usage / Development Setup
Before beginning, it is recommend
that these steps be carried out within a python virtual environment. This can be done by typing the following in the root directory of the project:
```
$ python3 -m venv venv
$ source ./venv/bin/activate
```

While still in the root directory, install all the necessary requirements by typing:
```
$ pip install -r requirements.txt
```

In order for passwords and other sensitive data to be hidden from version control a `config.ini` file must be created and put in the root of the project. These values relate to the database (cloud or otherwise) that is used.

The template file `config.ini.example` details what the `config.ini` should look like:
```ini
[DEFAULT]
HOST = 35.201.18.142
USER = root
PASSWORD = abcd1234
DATABASE = main

[TEST]
HOST = 35.201.18.142
USER = root
PASSWORD = abcd1234
DATABASE = test
```

### Master Pi
#### Running The Flask App
Navigate to the `/master_pi` folder and run the REST API and frontend by typing:
```
$ export FLASK_APP=app
$ flask run --host=0.0.0.0
```
You can then access the app by going to a browser and typing the Master Pi's IP, followed by the specified port.
E.g. `192.168.1.235:5000/`

#### Running The TCP Socket Server
Navigate to the `/master_pi` folder and run the server by typing:
```
$ python socket_server
```

#### Populating The Database
Data can be populated from the `/master_pi/tests/data.sql` file.
This can be done by navigating to the `/master_pi` folder typing:
```
$ flask init-db
```
Note: The the password of every user in the `data.sql` is `test`

#### Clearing The Database
To clear the database, navigate to the `/master_pi` folder and type:
```
$ flask clear-db
```

#### Running Unit Tests
Navigate to the `/master_pi` folder and run the unit tests by typing:
```
$ pytest
```

###  Agent Pi
#### Running The TCP Socket Client
Navigate to the `/agent_pi` folder and run the console application by typing:
```
$ python socket_client <ip_of_master_pi> <car_id>
```
The client requires two command line arguments - the IP of the Master Pi as well as the ID of the car the Agent Pi corresponds to.

#### Running Unit Tests
Navigate to the `/agent_pi` folder and run the unit tests by typing:
```
$ pytest
```

### Compiling Sphinx Documentation
Navigate to the `/docs` folder and compile the documentation by typing:
```
$ make html
```
From there you can view the docs by running the Flask application and going to the app's address followed by `/docs/index.html`
E.g. `192.168.1.235:5000/docs/index.html`
