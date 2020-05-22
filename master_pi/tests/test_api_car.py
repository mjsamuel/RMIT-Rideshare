import pytest

class TestApiCarEndpoints:
    def test_search(self, client):
        """Testing search returns all cars when no filter is supplied
        """

        response = client.get('/api/cars')
        expected_data = b'{"cars":[{"body_type":"SUV","colour":"Black","cost_per_hour":15,"id":1,"is_locked":true,"location":null,"make":"Toyota","no_seats":5},{"body_type":"Pickup","colour":"Silver","cost_per_hour":25,"id":2,"is_locked":true,"location":null,"make":"Tesla","no_seats":6},{"body_type":"Hatchback","colour":"Black","cost_per_hour":15,"id":3,"is_locked":true,"location":null,"make":"Toyota","no_seats":5}],"message":""}\n'

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
        expected_data = b'{"cars":[{"body_type":"SUV","colour":"Black","cost_per_hour":15,"id":1,"is_locked":true,"location":null,"make":"Toyota","no_seats":5},{"body_type":"Hatchback","colour":"Black","cost_per_hour":15,"id":3,"is_locked":true,"location":null,"make":"Toyota","no_seats":5}],"message":""}\n'

        assert (response.status == '200 OK')
        assert (response.data == expected_data)

    def test_search_cost_per_hour(self, client):
        """Testing search returns correct cars when filtering by cost per hour
        """

        response = client.get('/api/cars?cost_per_hour=25')
        expected_data = b'{"cars":[{"body_type":"Pickup","colour":"Silver","cost_per_hour":25,"id":2,"is_locked":true,"location":null,"make":"Tesla","no_seats":6}],"message":""}\n'

        assert (response.status == '200 OK')
        assert (response.data == expected_data)

    def test_search_no_seats(self, client):
        """Testing search returns correct cars when filtering by cost per hour
        """

        response = client.get('/api/cars?cost_per_hour=25')
        expected_data = b'{"cars":[{"body_type":"Pickup","colour":"Silver","cost_per_hour":25,"id":2,"is_locked":true,"location":null,"make":"Tesla","no_seats":6}],"message":""}\n'

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

        print(response.status)
        print(response.data)

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
