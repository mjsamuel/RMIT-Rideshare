import json, socket

class Client:
    """A class to represent a TCP socket client that connects to a server and
    for other code to interface with.

    :param host: The IP address of the Master Pi
    :type host: string
    :param car_id: The ID of the car that this Agent Pi corresponds to
    :type car_id: string
    """
    __PORT = 65000
    """The port that the server will listen on"""
    __server = None
    """A socket object for the server"""
    __client = None
    """A socket object for the client"""

    def __init__(self, host, car_id):
        """Constructor method
        """
        self.__host = host
        self.__car_id = car_id

    def connect_to_server(self):
        """Creates and returns a TCP socket connection to the Master Pi
        """
        address = (self.__host, self.__PORT)
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.connect(address)

    def disconnect_from_server(self):
        """Disconnects from the Master Pi server
        """
        self.__server.close()
        __server = None


    def login(self, username, password):
        """Sends user credentials to the Master Pi to log in.\n
        Sends the username and password values to the Master Pi via the TCP
        socket.\n
        The method then recieves a response from the server which is returned.

        :param username: The user's usernmae
        :type username: string
        :param password: The user's password
        :type password: string
        """
        # Indicating to Master Pi to begin login
        message = "Login"
        self.__server.sendall(message.encode())

        # Sending login credentials to Master Pi
        message = json.dumps({
            "username": username,
            "password": password
        })
        self.__server.sendall(message.encode())

        # Returning response
        data = self.__server.recv(4096)
        response = json.loads(data.decode())
        return response
