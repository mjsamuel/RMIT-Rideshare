import json, pytest, mock
from socket_client.client import Client

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
    def test_disconnect(self, mock_connection, socket_client):
        # Setting up mock object
        mock_connection.return_value = mock_connection
        
        # Code to be tested
        socket_client.connect_to_server()
        socket_client.disconnect_from_server()

        # Checking values are as expected
        mock_connection.close.assert_called()
