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
