import json, pytest, mock, pyqrcode, png, os, cv2
from socket_client.client import Client
from socket_client.qr_code_util import QrCodeUtil


@pytest.fixture
def socket_client():
    socket_client = Client("127.0.0.1", "1")
    return socket_client


class TestSocketClient:


    @mock.patch('socket_client.client.socket.socket')
    def test_start(self, mock_connection, socket_client):
        # Setting up mock object
        mock_connection.return_value = mock_connection

        # Code to be tested
        address = ("127.0.0.1", 65000)
        socket_client.connect_to_server()

        # Checking values are as expected
        mock_connection.connect.assert_called_with(address)
        assert(socket_client.get_server() is not None)


    @mock.patch('socket_client.client.socket.socket')
    def test_login(self, mock_connection, socket_client):
        server_response = {
            'message': 'Logged in',
            'user': 'test'
        }
        # Setting up mock object
        mock_connection.return_value = mock_connection
        mock_connection.recv.return_value = json.dumps(server_response).encode()

        # Code to be tested
        socket_client.connect_to_server()
        response = socket_client.login("test", "dummy")

        # Checking values are as expected
        assert(response == server_response)


    @mock.patch('socket_client.client.socket.socket')
    def test_login_bluetooth(self, mock_connection, socket_client):
        server_response = {
            'message': 'Logged in',
            'user': 'test'
        }
        # Dummy mac address
        mac_address = '18:F1:D8:E2:E9:6B'

        # Setting up mock object
        mock_connection.return_value = mock_connection
        mock_connection.recv.return_value = json.dumps(server_response).encode()

        # Code to be tested
        socket_client.connect_to_server()
        response = socket_client.login_via_bluetooth(mac_address)

        # Checking values are as expected
        assert (response == server_response)


    @mock.patch('socket_client.client.socket.socket')
    def test_disconnect(self, mock_connection, socket_client):
        # Setting up mock object
        mock_connection.return_value = mock_connection

        # Code to be tested
        socket_client.connect_to_server()
        socket_client.disconnect_from_server()

        # Checking values are as expected
        mock_connection.close.assert_called()


    @mock.patch('socket_client.client.socket.socket')
    def test_change_lock_status(self, mock_connection, socket_client):
        server_response = {
            'message': 'Car has been returned',
        }
        # Setting up mock object
        mock_connection.return_value = mock_connection
        mock_connection.recv.return_value = json.dumps(server_response).encode()

        # Code to be tested
        socket_client.connect_to_server()
        response = socket_client.change_lock_status("test", 1, "unlock")

        # Checking values are as expected
        assert(response == server_response['message'])


    @mock.patch('socket_client.client.socket.socket')
    def test_set_location(self, mock_connection, socket_client):
        server_response = {
            'message': 'Location has been updated',
        }
        # Setting up mock object
        mock_connection.return_value = mock_connection
        mock_connection.recv.return_value = json.dumps(server_response).encode()

        # Code to be tested
        socket_client.connect_to_server()
        response = socket_client.set_location(1, "32.426998,-81.754753")

        # Checking values are as expected
        assert(response == server_response['message'])

