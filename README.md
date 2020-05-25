<div align="center">
  <h1>
    <br>
     <img src="https://i.imgur.com/0EqVtUO.png" alt="Showoff Icon" height="125">
    <br>
    Programming Internet of Things<br> Assignment 3<br>
    <img src="https://travis-ci.com/matt-samuel-s3717393/IoT-Assignment3.svg?token=8bnx6syKrM5BbM1FTCfx&branch=develop"/>
   <br>
  </h1>
  <strong>Car Share IoT application</strong><br>
  <sub>Matthew Samuel (s3717393) Sakaowduan Artpru (s3609620), Oskar Floeck (s3725028) and Patrick Jones (s3661943)</sub>
</div>

## Dependencies
- [Python >= 3.5](https://www.python.org)

## Usage / Development Setup

Navigate to the root of the project and install all the necessary requirements by typing:
```
$ pip install -r requirements.txt
```
I'd also recommend you do this within a virtual environment

In order for passwords and other sensitive data to be hidden from version control a `config.ini` file must be created and put in the root of the project. These values relate to the Google cloud database as well as the encryption key used to encrypt user passwords.

The template file `config.ini.example` details what the `config.ini` should look like:
```ini
[DEFAULT]
HOST = 35.201.18.142
USER = root
PASSWORD = abcd1234
DATABASE = main-db

[TEST]
HOST = 35.201.18.142
USER = root
PASSWORD = abcd1234
DATABASE = test-db
```

### Master Pi
#### Running Flask Project
Navigate to the `/master_pi` folder and run the REST API and frontend code by typing:
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

#### Compiling Sphinx documentation
Navigate to the `/docs` folder and compile the documentation by typing:
```
$ make html
```
From there you can view the docs by running the Flask application and going to the app's adress followed by `/docs/index.html`
E.g. `192.168.1.235:5000/docs/index.html`

#### Running Unit Tests
Navigate to the `/master_pi` folder and run the unit tests by typing:
```
$ pytest
```

###  Agent Pi
#### Running The TCP Socket Client
Navigate to the `/agent_pi` folder and run the console application by typing:
```
$ python socket_client <ip of master pi> <car id>
```
The client requires two command line arguments - the IP of the Master Pi as well as the ID of the car the Agent Pi corresponds to.

#### Running Unit Tests
Navigate to the `/agent_pi` folder and run the unit tests by typing:
```
$ pytest
```
