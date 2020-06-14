import pytest, json

class TestApiIssueEndpoints:
    def test_new_issue_success(self, client):
        """Testing that reporting an issue succeeds when called with the correct
        information
        """
        response = client.post(
            '/api/issue',
            json={
                "car_id": 1,
                "username": "admin",
                "details": "Broken tail light",
            }
        )
        expected_data = b'{"message":"Success"}\n'

        assert (response.status == '200 OK')
        assert (response.data == expected_data)


    def test_new_issue_fail_invalid_role(self, client):
        """Testing that reporting an issue fails when not the user requesting
        the update is not an admin
        """
        response = client.post(
            '/api/issue',
            json={
                "car_id": 1,
                "username": "dummy",
                "details": "Broken tail light",
            }
        )
        expected_data = b'{"message":{"user":["User is not an admin."]}}\n'

        assert (response.status == '401 UNAUTHORIZED')
        assert (response.data == expected_data)


    def test_get_issue(self, client):
        """Testing that the get issue endpoint returns the correct issue when
        supplied with an id
        """
        response = client.get('/api/issue?id=1')
        expected_data = b'{"issues":{"car":{"body_type":"SUV","colour":"Black","cost_per_hour":15,"id":1,"is_locked":true,"location":"-37.808880,144.965179","make":"Toyota","no_seats":5},"car_id":1,"details":"Broken tail light","id":1,"resolved":true,"time":"2020-05-09T02:22:51"}}\n'

        assert (response.status == '200 OK')
        assert (response.data == expected_data)


    def test_get_issues(self, client):
        """Testing that the get issue endpoint returns the every issue when
        not given an id
        """
        response = client.get('/api/issue')
        expected_data = b'{"issues":[{"car":{"body_type":"SUV","colour":"Black","cost_per_hour":15,"id":1,"is_locked":true,"location":"-37.808880,144.965179","make":"Toyota","no_seats":5},"car_id":1,"details":"Flat tire","id":3,"resolved":false,"time":"2020-06-01T02:22:51"},{"car":{"body_type":"SUV","colour":"Black","cost_per_hour":15,"id":1,"is_locked":true,"location":"-37.808880,144.965179","make":"Toyota","no_seats":5},"car_id":1,"details":"Broken tail light","id":1,"resolved":true,"time":"2020-05-09T02:22:51"},{"car":{"body_type":"Pickup","colour":"Silver","cost_per_hour":25,"id":2,"is_locked":true,"location":"-37.810219,144.961395","make":"Tesla","no_seats":6},"car_id":2,"details":"Battery is dead","id":2,"resolved":true,"time":"2020-05-07T02:22:51"}]}\n'

        assert (response.status == '200 OK')
        assert (response.data == expected_data)
