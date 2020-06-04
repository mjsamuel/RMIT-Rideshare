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

        expected_data = b'{"message":"Logged in successfully","user":{"role":"default","username":"dummy"}}\n'

        assert (response.status == '200 OK')
        assert (response.data == expected_data)

    def test_login_success_admin(self, client):
        """Testing for a sucessful login for an admin account
        """

        response = client.post(
            '/api/login',
            json={
                "username": "admin",
                "password": "test"
            }
        )

        expected_data = b'{"message":"Logged in successfully","user":{"role":"admin","username":"admin"}}\n'

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

        expected_data = b'{"message":{"username":["Missing data for required field."]},"user":null}\n'

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

        expected_data = b'{"message":{"password":["Missing data for required field."]},"user":null}\n'

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

        expected_data = b'{"message":{"user":["Incorrect password."]},"user":null}\n'

        assert (response.status == '401 UNAUTHORIZED')
        assert (response.data == expected_data)

    def test_register_success(self, app, client):
        """Testing for a sucessful registration
        """

        response = client.post(
            '/api/user',
            json={
                "username": "newuser",
                "f_name": "Jane",
                "l_name": "Doe",
                "email": "abcd@gmail.com",
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
                "f_name": "Jane",
                "l_name": "Doe",
                "email": "abcd@gmail.com",
                "password": "abcd",
                "confirm_password": "dcba"
            }
        )

        expected_data = b'{"message":{"_schema":["Passwords do not match."]},"user":null}\n'

        assert (response.status == '400 BAD REQUEST')
        assert (response.data == expected_data)

    def test_register_fail_missing_username(self, app, client):
        """Testing for a unsucessful registration due to missing username
        """

        response = client.post(
            '/api/user',
            json={
                "f_name": "Jane",
                "l_name": "Doe",
                "email": "abcd@gmail.com",
                "password": "abcd",
                "confirm_password": "abcd"
            }
        )

        expected_data = b'{"message":{"username":["Missing data for required field."]},"user":null}\n'

        assert (response.status == '400 BAD REQUEST')
        assert (response.data == expected_data)

    def test_register_fail_missing_f_name(self, app, client):
        """Testing for a unsucessful registration due to missing first name
        """

        response = client.post(
            '/api/user',
            json={
                "username": "newuser",
                "l_name": "Doe",
                "email": "abcd@gmail.com",
                "password": "abcd",
                "confirm_password": "abcd"
            }
        )

        expected_data = b'{"message":{"f_name":["Missing data for required field."]},"user":null}\n'

        assert (response.status == '400 BAD REQUEST')
        assert (response.data == expected_data)

    def test_register_fail_missing_l_name(self, app, client):
        """Testing for a unsucessful registration due to missing last name
        """

        response = client.post(
            '/api/user',
            json={
                "username": "newuser",
                "f_name": "John",
                "email": "abcd@gmail.com",
                "password": "abcd",
                "confirm_password": "abcd"
            }
        )

        expected_data = b'{"message":{"l_name":["Missing data for required field."]},"user":null}\n'

        assert (response.status == '400 BAD REQUEST')
        assert (response.data == expected_data)

    def test_register_fail_missing_email(self, app, client):
        """Testing for a unsucessful registration due to missing email
        """

        response = client.post(
            '/api/user',
            json={
                "username": "newuser",
                "f_name": "John",
                "l_name": "Doe",
                "password": "abcd",
                "confirm_password": "abcd"
            }
        )

        expected_data = b'{"message":{"email":["Missing data for required field."]},"user":null}\n'

        assert (response.status == '400 BAD REQUEST')
        assert (response.data == expected_data)

    def test_register_fail_bad_email(self, app, client):
        """Testing for a unsucessful registration due to email not being in the correct format
        """

        response = client.post(
            '/api/user',
            json={
                "username": "newuser",
                "f_name": "John",
                "l_name": "Doe",
                "email": "email.com",
                "password": "abcd",
                "confirm_password": "abcd"
            }
        )

        expected_data = b'{"message":{"email":["Not a valid email address."]},"user":null}\n'

        assert (response.status == '400 BAD REQUEST')
        assert (response.data == expected_data)

    def test_register_fail_missing_password(self, app, client):
        """Testing for a unsucessful registration due to missing password
        """

        response = client.post(
            '/api/user',
            json={
                "username": "newuser",
                "f_name": "Jane",
                "l_name": "Doe",
                "email": "abcd@gmail.com",
                "confirm_password": "abcd"
            }
        )

        expected_data = b'{"message":{"password":["Missing data for required field."]},"user":null}\n'

        assert (response.status == '400 BAD REQUEST')
        assert (response.data == expected_data)

    def test_user_register_fail_missing_confirmed_password(self, app, client):
        """Testing for a unsucessful registration due to missing confirmed password
        """

        response = client.post(
            '/api/user',
            json={
                "username": "newuser",
                "f_name": "Jane",
                "l_name": "Doe",
                "email": "abcd@gmail.com",
                "password": "abcd"
            }
        )

        expected_data = b'{"message":{"confirm_password":["Missing data for required field."]},"user":null}\n'

        assert (response.status == '400 BAD REQUEST')
        assert (response.data == expected_data)

    def test_user_get_success(self, client):
        response = client.get('/api/user?username=dummy')
        expected_data = b'{"message":"User found","user":{"role":"default","username":"dummy"}}\n'

        assert (response.status == '200 OK')
        assert (response.data == expected_data)

    def test_user_get_fail(self, client):
        response = client.get('/api/user?username=unregistered_user')
        expected_data = b'{"message":"User not found","user":null}\n'

        assert (response.status == '404 NOT FOUND')
        assert (response.data == expected_data)
