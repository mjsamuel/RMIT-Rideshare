import pytest

class TestApiUserEndpoints:
    def test_login_success(self, client):
        """Testing for a sucessful login with an already registered user
        """

        response = client.post(
            '/api/login',
            json={
                "username": "dummy",
                "password": "test"
            }
        )

        expected_data = b'{"message":"Logged in successfully","user":{"username":"dummy"}}\n'

        assert (response.status == '200 OK')
        assert (response.data == expected_data)

    def test_login_fail_missing_username(self, client):
        """Testing for a unsucessful login due to a missing username
        """

        response = client.post(
            '/api/login',
            json={
                "password": "test"
            }
        )

        expected_data = b'{"message":"Missing username","user":null}\n'

        assert (response.status == '400 BAD REQUEST')
        assert (response.data == expected_data)

    def test_login_fail_missing_password(self, client):
        """Testing for a unsucessful login due to a missing password
        """

        response = client.post(
            '/api/login',
            json={
                "username": "dummy"
            }
        )

        expected_data = b'{"message":"Missing password","user":null}\n'

        assert (response.status == '400 BAD REQUEST')
        assert (response.data == expected_data)

    def test_login_fail_wrong_password(self, client):
        """Testing for a unsucessful login due to a missing password
        """

        response = client.post(
            '/api/login',
            json={
                "username": "dummy",
                "password": "abcd"
            }
        )

        expected_data = b'{"message":"Incorrect password","user":null}\n'

        assert (response.status == '401 UNAUTHORIZED')
        assert (response.data == expected_data)

    def test_register_success(self, app, client):
        """Testing for a sucessful registration
        """

        response = client.post(
            '/api/user',
            json={
                "username": "newuser",
                "password": "abcd",
                "confirm_password": "abcd"
            }
        )

        expected_data = b'{"message":"Registered user successfully","user":{"username":"newuser"}}\n'

    def test_register_fail_password(self, app, client):
        """Testing for a unsucessful registration due to passwords not matching
        """

        response = client.post(
            '/api/user',
            json={
                "username": "newuser",
                "password": "abcd",
                "confirm_password": "dcba"
            }
        )

        expected_data = b'{"message":"Passwords do not match","user":null}\n'

        assert (response.status == '400 BAD REQUEST')
        assert (response.data == expected_data)

    def test_register_fail_missing_username(self, app, client):
        """Testing for a unsucessful registration due to missing username
        """

        response = client.post(
            '/api/user',
            json={
                "password": "abcd",
                "confirm_password": "dcba"
            }
        )

        expected_data = b'{"message":"Missing username","user":null}\n'

        assert (response.status == '400 BAD REQUEST')
        assert (response.data == expected_data)

    def test_register_fail_missing_password(self, app, client):
        """Testing for a unsucessful registration due to missing password
        """

        response = client.post(
            '/api/user',
            json={
                "username": "newuser",
                "confirm_password": "dcba"
            }
        )

        expected_data = b'{"message":"Missing password","user":null}\n'

        assert (response.status == '400 BAD REQUEST')
        assert (response.data == expected_data)

    def test_user_register_fail_missing_confirmedpassword(self, app, client):
        """Testing for a unsucessful registration due to missing confirmed password
        """

        response = client.post(
            '/api/user',
            json={
                "username": "newuser",
                "password": "abcd"
            }
        )

        expected_data = b'{"message":"Missing confirmed password","user":null}\n'

        assert (response.status == '400 BAD REQUEST')
        assert (response.data == expected_data)

    def test_user_get_success(self, client):
        response = client.get('/api/user?username=dummy')
        expected_data = b'{"message":"User found","user":{"username":"dummy"}}\n'

        assert (response.status == '200 OK')
        assert (response.data == expected_data)

    def test_user_get_fail(self, client):
        response = client.get('/api/user?username=unregistered_user')
        expected_data = b'{"message":"User not found","user":null}\n'

        assert (response.status == '404 NOT FOUND')
        assert (response.data == expected_data)
