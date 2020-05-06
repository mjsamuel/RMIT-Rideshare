
<div align="center">
  <h1>
    <br>
     <img src="https://i.imgur.com/0EqVtUO.png" alt="Showoff Icon" height="125">
    <br>
    Programming Internet of Things<br> Assignment 2
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
In order for passwords and other sensitive data to be hidden from version control a `config.ini` file must be created and put in the root of the project. These values relate to the Google cloud database as well as the encryption key used to encrypt user passwords.

The template file `config.ini.example` details what the `config.ini` should look like:
```ini
[DEFAULT]
HOST = 35.201.18.142
USER = root
PASSWORD = abcd1234
DATABASE = main-db
ENCRYPTION_KEY = abcd1234

[TEST]
HOST = 35.201.18.142
USER = root
PASSWORD = abcd1234
DATABASE = test-db
ENCRYPTION_KEY = abcd1234
```

### Master Pi
Navigate to the `/master_pi` folder and run the REST API and frontend code by typing:
```
$ export FLASK_APP=app
$ flask run --host=0.0.0.0
```
You can then access the app by going to a browser and typing the Master Pi's IP, followed by the specified port.
E.g `192.168.1.235:5000/`

###  Agent Pi
Navigate to the `/agent_pi` folder and run the console application by typing:
```
$ python3 main.py
```