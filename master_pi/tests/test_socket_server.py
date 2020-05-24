import json, pytest, mock
from socket_server.server import Server

# Fixtures specific to the socket server tests
@pytest.fixture
def socket_server():
    server = Server()
    server.start_socket_server()

    yield server

    server.stop_socket_server()

class TestSocketServer:
    def test_start_socket_server(self, socket_server):
        """Tests that the server socket starts successfully
        """
        assert(socket_server.get_server() is not None)
        assert(socket_server.get_client() is None)

    @mock.patch('socket_server.server.socket.socket.accept')
    def test_wait_for_connection(self, mock_connection, socket_server):
        """Tests that the server socket can be connected to successfully
        """
        # Setting up mock object
        mock_connection.return_value = ("client", "127.0.0.1")

        # Code to be tested
        address = socket_server.wait_for_connection()

        assert(address == "127.0.0.1")
        assert(socket_server.get_client() is not None)

    @mock.patch('socket_server.server.socket.socket.accept')
    def test_wait_for_instruction(self, mock_connection, socket_server):
        """Tests that the instruction sent to the server is correct
        """
        # Setting up mock object
        mock_connection.return_value = (mock_connection, "127.0.0.1")
        mock_connection.recv.return_value = "Login".encode()

        # Code to be tested
        socket_server.wait_for_connection()
        instruction = socket_server.wait_for_instruction()

        assert(instruction == "Login")

    @mock.patch('socket_server.server.socket.socket.accept')
    @mock.patch('socket_server.server.requests.post')
    def test_login(self, mock_post, mock_connection, socket_server):
        """Tests that the socket calls the API endpoint for logging in and
        returns it's response correctly
        """
        api_response = json.dumps({
            "user": "test",
            "message": "Logged in"
        })

        # Setting up mock objects
        mock_connection.return_value = (mock_connection, "127.0.0.1")
        mock_connection.recv.return_value = json.dumps({
            "username": "test",
            "password": "dummy"
        }).encode()
        mock_post.status_code.return_value = 200
        mock_post.return_value.text = api_response

        # Code to be tested
        socket_server.wait_for_connection()
        response = socket_server.login()

        mock_connection.sendall.assert_called_with(api_response.encode())

    @mock.patch('socket_server.server.socket.socket.accept')
    @mock.patch('socket_server.server.Server.receive_image_from_client')
    @mock.patch('socket_server.face_recognition_util.cv2.imwrite')
    def test_add_face(self, mock_cv2, mock_image, mock_connection, socket_server):
        """Tests to make sure that images are being saved
        """
        # Setting up mock objects
        mock_connection.return_value = (mock_connection, "127.0.0.1")
        mock_image.return_value = {
            "username": "test",
            "image": "image"
        }

        # Code to be tested
        socket_server.wait_for_connection()
        socket_server.add_face()

        # Making sure that the function to save to the dataset folder is called
        mock_cv2.assert_called()

    @mock.patch('socket_server.server.socket.socket.accept')
    @mock.patch('socket_server.server.requests.post')
    def test_return_car(self, mock_post, mock_connection, socket_server):
        """Tests that the socket calls the API endpoint for returning a car and
        returns it's response correctly
        """
        api_response = json.dumps({
            "message": "Car is returned"
        })

        # Setting up mock objects
        mock_connection.return_value = (mock_connection, "127.0.0.1")
        mock_connection.recv.return_value = json.dumps({
            "username": "test",
            "car_id": "1",
            "method": "return"
        }).encode()
        mock_post.status_code.return_value = 200
        mock_post.return_value.text = api_response

        # Code to be tested
        socket_server.wait_for_connection()
        response = socket_server.change_lock_status()

        mock_connection.sendall.assert_called_with(api_response.encode())

    @mock.patch('socket_server.server.socket.socket.accept')
    @mock.patch('socket_server.server.requests.post')
    def test_unlock_car(self, mock_post, mock_connection, socket_server):
        """Tests that the socket calls the API endpoint for unlocking a car and
        returns it's response correctly
        """
        api_response = json.dumps({
            "message": "Car is unlocked"
        })

        # Setting up mock objects
        mock_connection.return_value = (mock_connection, "127.0.0.1")
        mock_connection.recv.return_value = json.dumps({
            "username": "test",
            "car_id": "1",
            "method": "unlock"
        }).encode()
        mock_post.status_code.return_value = 200
        mock_post.return_value.text = api_response

        # Code to be tested
        socket_server.wait_for_connection()
        response = socket_server.change_lock_status()

        mock_connection.sendall.assert_called_with(api_response.encode())

    @mock.patch('socket_server.server.socket.socket.accept')
    @mock.patch('socket_server.server.requests.post')
    def test_change_car_location(self, mock_post, mock_connection, socket_server):
        """Tests that the socket calls the API endpoint for changing the location
        of a car and returns it's response correctly
        """
        api_response = json.dumps({
            "message": "Location has been changed"
        })

        # Setting up mock objects
        mock_connection.return_value = (mock_connection, "127.0.0.1")
        mock_connection.recv.return_value = json.dumps({
            "car_id": "1",
            "location": "return"
        }).encode()
        mock_post.status_code.return_value = 200
        mock_post.return_value.text = api_response

        # Code to be tested
        socket_server.wait_for_connection()
        response = socket_server.change_car_location()

        mock_connection.sendall.assert_called_with(api_response.encode())
