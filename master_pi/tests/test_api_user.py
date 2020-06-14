import pytest


class TestApiUserEndpoints:


    def test_login_success(self, client):
        """Testing for a successful login with an already registered user
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


    def test_login_bluetooth_success(self, client):
        """Testing for a successful bluetooth login with an already registered user
        """

        response = client.post(
            '/api/login-bluetooth',
            json={
                "username": "dummy",
                "mac_address": "18:F1:D8:E2:E9:6B"
            }
        )

        expected_data = b'{"message":"Logged in successfully","user":{"role":"default","username":"dummy"}}\n'
        print(response.data)

        assert (response.status == '200 OK')
        assert (response.data == expected_data)


    def test_login_bluetooth_fail(self, client):
        """Testing for a successful bluetooth login with an already registered user
        """

        response = client.post(
            '/api/login-bluetooth',
            json={
                "username": "dummy",
                "mac_address": "37:F4:C8:E2:E5:9B"
            }
        )

        expected_data = b'{"message":"ERROR: Bluetooth device is not registered to a user","user":null}\n'

        assert (response.status == '401 UNAUTHORIZED')
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
        """Testing for a successful registration
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


    def test_register_bluetooth_success(self, app, client):
        """Testing for successful bluetooth registration.
        """

        response = client.post(
            '/api/register_bluetooth',
            json={
                "username": "dummy",
                "mac_address": "18:F1:D8:E2:E9:6B"
            }
        )

        expected_data = b'{"message":"User MAC Address updated","user":{"username":"dummy"}}\n'

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
        expected_data = b'{"users":{"email":"dummyemail@gmail.com","f_name":"First","l_name":"Last","role":"default","username":"dummy"}}\n'

        assert (response.status == '200 OK')
        assert (response.data == expected_data)


    def test_user_get_fail(self, client):
        response = client.get('/api/user?username=unregistered_user')
        expected_data = b'{"users":{}}\n'

        assert (response.status == '200 OK')
        assert (response.data == expected_data)


    def test_user_query_email(self, client):
        response = client.get('/api/user?email=dummyemail@gmail.com')
        expected_data = b'{"users":[{"email":"dummyemail@gmail.com","f_name":"First","l_name":"Last","role":"default","username":"dummy"}]}\n'

        assert (response.status == '200 OK')
        assert (response.data == expected_data)


    def test_user_query_role(self, client):
        response = client.get('/api/user?role=admin')
        expected_data = b'{"users":[{"email":"admin@gmail.com","f_name":"First","l_name":"Last","role":"admin","username":"admin"}]}\n'

        assert (response.status == '200 OK')
        assert (response.data == expected_data)


    def test_user_query_fuzzy_name(self, client):
        response = client.get('/api/user?fuzzy_username=dum')
        expected_data = b'{"users":[{"email":"dummyemail@gmail.com","f_name":"First","l_name":"Last","role":"default","username":"dummy"}]}\n'

        assert (response.status == '200 OK')
        assert (response.data == expected_data)


    def test_update_user_success(self, client):
        """Testing for a successful update user by the admin
        """

        response = client.put(
            '/api/user',
            json={
                "admin_username": "admin",
                "confirm_password": "test",
                "email": "dummyemail@gmail.com",
                "f_name": "First",
                "l_name": "Last",
                "password": "test",
                "role": "3",
                "username": "dummy"
            }
        )

        expected_data = b'{"message":"Success"}\n'

        assert (response.status == '200 OK')
        assert (response.data == expected_data)

    def test_update_user_missing_fields(self, client):
        """Testing that updating a user fails when missing the required fields
        """
        response = client.put(
            '/api/user',
            json={
                "admin_username": "admin",
                "confirm_password": "1234",
                "email": "dummyemail@gmail.com",
                "f_name": "First",
                "l_name": "",
                "password": "1234",
                "role": "3",
                "username": ""
            }
        )
        expected_data = b'{"message":{"l_name":["Missing username."],"username":["Missing username."]}}\n'

        assert (response.status == '400 BAD REQUEST')
        assert (response.data == expected_data)

    def test_update_user_fail_invalid_role(self, client):
        """Testing for a unsucessful update user due to not being an admin
        """

        response = client.put(
            '/api/user',
            json={
                "admin_username": "dummy",
                "confirm_password": "test",
                "email": "dummyemail@gmail.com",
                "f_name": "First",
                "l_name": "Last",
                "password": "test",
                "role": "3",
                "username": "dummy"
            }
        )

        expected_data = b'{"message":{"user":["User is not an admin."]}}\n'

        assert (response.status == '401 UNAUTHORIZED')
        assert (response.data == expected_data)

    def test_delete_user_fail_invalid_role(self, client):
        """Testing that deleting a user fails when not the user requesting the
        update is not an admin
        """
        response = client.delete(
            '/api/user',
            json={
                "admin_username": "dummy",
                "username": "dummy"
            }
        )
        expected_data = b'{"message":{"user":["User is not an admin."]}}\n'

        assert (response.status == '401 UNAUTHORIZED')
        assert (response.data == expected_data)


    def test_delete_user_success(self, client):
        """Testing that deleting user succeeds with the correct
        information
        """
        response = client.delete(
            '/api/user',
            json={
                "admin_username": "admin",
                "username": "dummy"
            }
        )
        expected_data = b'{"message":"Success"}\n'

        assert (response.status == '200 OK')
        assert (response.data == expected_data)

    