import pytest, json

class TestApiCarEndpoints:
    def test_search(self, client):
        """Testing search returns all cars when no filter is supplied
        """

        response = client.get('/api/cars')
        expected_data = b'{"cars":[{"body_type":"SUV","colour":"Black","cost_per_hour":15,"id":1,"is_locked":true,"location":null,"make":"Toyota","no_seats":5},{"body_type":"Pickup","colour":"Silver","cost_per_hour":25,"id":2,"is_locked":true,"location":null,"make":"Tesla","no_seats":6},{"body_type":"Hatchback","colour":"Black","cost_per_hour":15,"id":3,"is_locked":true,"location":null,"make":"Toyota","no_seats":5},{"body_type":"Sedan","colour":"Green","cost_per_hour":25,"id":4,"is_locked":true,"location":null,"make":"Honda","no_seats":5},{"body_type":"Hatchback","colour":"Black","cost_per_hour":40,"id":5,"is_locked":true,"location":null,"make":"Mercedes","no_seats":5},{"body_type":"Supercar","colour":"Red","cost_per_hour":65,"id":6,"is_locked":true,"location":null,"make":"Ferrari","no_seats":2},{"body_type":"Coupe","colour":"White","cost_per_hour":25,"id":7,"is_locked":true,"location":null,"make":"Mazda","no_seats":4},{"body_type":"Cabriolet","colour":"Black","cost_per_hour":30,"id":8,"is_locked":true,"location":null,"make":"BMW","no_seats":5},{"body_type":"Sedan","colour":"Yellow","cost_per_hour":35,"id":9,"is_locked":true,"location":null,"make":"Renault","no_seats":5},{"body_type":"Truck","colour":"Black","cost_per_hour":65,"id":10,"is_locked":true,"location":null,"make":"Porsche","no_seats":2}],"message":""}\n'

        assert (response.status == '200 OK')
        assert (response.data == expected_data)


    def test_search_body_type(self, client):
        """Testing search returns correct cars when filtering by body type
        """

        response = client.get('/api/cars?body_type=SUV')
        expected_data = b'{"cars":[{"body_type":"SUV","colour":"Black","cost_per_hour":15,"id":1,"is_locked":true,"location":null,"make":"Toyota","no_seats":5}],"message":""}\n'

        assert (response.status == '200 OK')
        assert (response.data == expected_data)


    def test_search_colour(self, client):
        """Testing search returns correct cars when filtering by colour
        """

        response = client.get('/api/cars?colour=black')
        expected_data = b'{"cars":[{"body_type":"SUV","colour":"Black","cost_per_hour":15,"id":1,"is_locked":true,"location":null,"make":"Toyota","no_seats":5},{"body_type":"Hatchback","colour":"Black","cost_per_hour":15,"id":3,"is_locked":true,"location":null,"make":"Toyota","no_seats":5},{"body_type":"Hatchback","colour":"Black","cost_per_hour":40,"id":5,"is_locked":true,"location":null,"make":"Mercedes","no_seats":5},{"body_type":"Cabriolet","colour":"Black","cost_per_hour":30,"id":8,"is_locked":true,"location":null,"make":"BMW","no_seats":5},{"body_type":"Truck","colour":"Black","cost_per_hour":65,"id":10,"is_locked":true,"location":null,"make":"Porsche","no_seats":2}],"message":""}\n'

        assert (response.status == '200 OK')
        assert (response.data == expected_data)


    def test_search_cost_per_hour(self, client):
        """Testing search returns correct cars when filtering by cost per hour
        """

        response = client.get('/api/cars?cost_per_hour=25')
        expected_data = b'{"cars":[{"body_type":"Pickup","colour":"Silver","cost_per_hour":25,"id":2,"is_locked":true,"location":null,"make":"Tesla","no_seats":6},{"body_type":"Sedan","colour":"Green","cost_per_hour":25,"id":4,"is_locked":true,"location":null,"make":"Honda","no_seats":5},{"body_type":"Coupe","colour":"White","cost_per_hour":25,"id":7,"is_locked":true,"location":null,"make":"Mazda","no_seats":4}],"message":""}\n'

        assert (response.status == '200 OK')
        assert (response.data == expected_data)


    def test_search_no_seats(self, client):
        """Testing search returns correct cars when filtering by cost per hour
        """

        response = client.get('/api/cars?cost_per_hour=25')
        expected_data = b'{"cars":[{"body_type":"Pickup","colour":"Silver","cost_per_hour":25,"id":2,"is_locked":true,"location":null,"make":"Tesla","no_seats":6},{"body_type":"Sedan","colour":"Green","cost_per_hour":25,"id":4,"is_locked":true,"location":null,"make":"Honda","no_seats":5},{"body_type":"Coupe","colour":"White","cost_per_hour":25,"id":7,"is_locked":true,"location":null,"make":"Mazda","no_seats":4}],"message":""}\n'

        assert (response.status == '200 OK')
        assert (response.data == expected_data)


    def test_unlock_success(self, client, ):
        """Testing that unlocking a car succeeds when the user has booked the car
        """
        # Creating booking for the user
        client.post(
            '/api/booking',
            json={
                "car_id": 1,
                "username": "dummy",
                "duration": 2
            }
        )

        # Unlocking the car
        response = client.post(
            '/api/unlock',
            json={
                "username": "dummy",
                "car_id": 1
            }
        )
        expected_data = b'{"message":"Car has been unlocked"}\n'

        assert (response.status == '200 OK')
        assert (response.data == expected_data)


    def test_unlock_fail_already_unlocked(self, client, ):
        """Testing that unlocking a car fails when the user has already unlocked it
        """
        # Creating booking for the user
        client.post(
            '/api/booking',
            json={
                "car_id": 1,
                "username": "dummy",
                "duration": 2
            }
        )

        # Unlocking the car
        data = {
            "username": "dummy",
            "car_id": 1
        }
        client.post('/api/unlock', json= data)
        # Unlocking the car again
        response = client.post('/api/unlock', json= data)

        expected_data = b'{"message":"ERROR: The car is already unlocked"}\n'

        assert (response.status == '409 CONFLICT')
        assert (response.data == expected_data)


    def test_unlock_fail_not_booked(self, client, ):
        """Testing that unlocking a car fails when the user has not booked it
        """
        # Unlocking the car
        response = client.post(
            '/api/unlock',
            json={
                "username": "dummy",
                "car_id": 1
            }
        )
        expected_data = b'{"message":"ERROR: You have not booked this car"}\n'

        assert (response.status == '403 FORBIDDEN')
        assert (response.data == expected_data)


    def test_return_success(self, client, ):
        """Testing that returning a car succeeds when the user has unlocked the car
        """
        # Creating booking for the user
        client.post(
            '/api/booking',
            json={
                "car_id": 1,
                "username": "dummy",
                "duration": 2
            }
        )

        # Unlocking the car
        client.post(
            '/api/unlock',
            json={
                "username": "dummy",
                "car_id": 1
            }
        )

        # Returning the car
        response = client.post(
            '/api/return',
            json={
                "username": "dummy",
                "car_id": 1
            }
        )
        expected_data = b'{"message":"Car has been returned"}\n'

        assert (response.status == '200 OK')
        assert (response.data == expected_data)


    def test_return_fail_already_returned(self, client, ):
        """Testing that returning a car fails when the user has already returned
        the car
        """
        # Creating booking for the user
        client.post(
            '/api/booking',
            json={
                "car_id": 1,
                "username": "dummy",
                "duration": 2
            }
        )

        # Unlocking the car
        client.post(
            '/api/unlock',
            json={
                "username": "dummy",
                "car_id": 1
            }
        )

        # Returning the car
        data = {
            "username": "dummy",
            "car_id": 1
        }
        client.post('/api/return', json=data)
        # Returning it again
        response = client.post('/api/return', json=data)
        expected_data = b'{"message":"ERROR: The car has already been returned"}\n'

        assert (response.status == '409 CONFLICT')
        assert (response.data == expected_data)


    def test_return_fail_not_booked(self, client, ):
        """Testing that returning a car fails when the user has not booked the car
        """
        # Returning the car
        response = client.post(
            '/api/return',
            json={
                "username": "dummy",
                "car_id": 3
            }
        )
        expected_data = b'{"message":"ERROR: You have not booked this car"}\n'

        assert (response.status == '403 FORBIDDEN')
        assert (response.data == expected_data)


    def test_change_car_location(self, client):
        """Testing that changing a car's location succeeds
        """
        location = "32.426998,-81.754753"
        post_response = client.post(
            '/api/setlocation',
            json={
                "car_id": "1",
                "location": location
            }
        )
        expected_post_response = b'{"message":"Car location updated"}\n'
        get_response = json.loads(client.get('/api/cars?id=1').data)

        assert (post_response.status == '200 OK')
        assert (post_response.data == expected_post_response)
        assert (get_response['cars']['location'] == location)


    def test_change_car_fail_invalid_id(self, client):
        """Testing that changing a car's location fails due to an invalid id
        """
        response = client.post(
            '/api/setlocation',
            json={
                "car_id": "245",
                "location": "32.426998,-81.754753"
            }
        )
        expected_data = b'{"message":"ERROR: Car does not exist"}\n'

        assert (response.status == '404 NOT FOUND')
        assert (response.data == expected_data)


    def test_put_car(self, client):
        """Testing that updating a car's information succeeds with the correct
        information
        """
        response = client.put(
            '/api/car',
            json={
                "car_id": "1",
                "username": "admin",
                "make": "Toyota",
                "body_type": "SUV",
                "colour": "Black",
                "no_seats": 5,
                "location": "32.426998,-81.754753",
                "cost_per_hour": 20
            }
        )
        expected_data = b'{"message":"Success"}\n'

        assert (response.status == '200 OK')
        assert (response.data == expected_data)


    def test_put_car_fail_invalid_role(self, client):
        """Testing that updating a car fails when not the user requesting then
        update is not an admin
        """
        response = client.put(
            '/api/car',
            json={
                "car_id": "1",
                "username": "dummy",
                "make": "Toyota",
                "body_type": "SUV",
                "colour": "Black",
                "no_seats": 5,
                "location": "32.426998,-81.754753",
                "cost_per_hour": 20
            }
        )
        expected_data = b'{"message":{"user":["User is not an admin."]}}\n'

        assert (response.status == '401 UNAUTHORIZED')
        assert (response.data == expected_data)


    def test_put_car_fail_invalid_location(self, client):
        """Testing that updating a car fails when inputting an invalid location
        """
        response = client.put(
            '/api/car',
            json={
                "car_id": "1",
                "username": "dummy",
                "make": "Toyota",
                "body_type": "SUV",
                "colour": "Black",
                "no_seats": 5,
                "location": "invalid,location",
                "cost_per_hour": 20
            }
        )
        expected_data = b'{"message":{"location":["Location is not a valid latitude/longitude."]}}\n'

        assert (response.status == '400 BAD REQUEST')
        assert (response.data == expected_data)


    def test_put_car_fail_invalid_ints(self, client):
        """Testing that updating a car fails when inputting an invalid number of
        seats and invalid cost per hour
        """
        response = client.put(
            '/api/car',
            json={
                "car_id": "1",
                "username": "admin",
                "make": "Toyota",
                "body_type": "SUV",
                "colour": "Black",
                "no_seats": -5,
                "location": "32.426998,-81.754753",
                "cost_per_hour": -20
            }
        )
        expected_data = b'{"message":{"cost_per_hour":["Cost per hour must be a positive integer."],"no_seats":["Number of seats must be a positive integer."]}}\n'

        assert (response.status == '400 BAD REQUEST')
        assert (response.data == expected_data)


    def test_put_car_fail_missing_fields(self, client):
        """Testing that updating a car fails when missing the required fields
        """
        response = client.put(
            '/api/car',
            json={
                "car_id": "1",
                "username": "admin",
                "make": "",
                "body_type": "",
                "colour": "",
                "no_seats": -5,
                "location": "",
                "cost_per_hour": -20
            }
        )
        expected_data = b'{"message":{"body_type":["Missing body type."],"colour":["Missing colour."],"cost_per_hour":["Cost per hour must be a positive integer."],"location":["Missing location."],"make":["Missing make."],"no_seats":["Number of seats must be a positive integer."]}}\n'

        assert (response.status == '400 BAD REQUEST')
        assert (response.data == expected_data)
