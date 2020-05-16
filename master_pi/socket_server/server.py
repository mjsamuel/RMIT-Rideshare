import json, requests, socket

class Server:
    """A class to represent a TCP socket server for a client to interact with
    and for the other code to interface with
    """
    __HOST = ""
    """The IP address that the server will listen on"""
    __PORT = 65000
    """The port that the server will listen on"""
    __server = None
    """A socket object for the server"""
    __client = None
    """A socket object for the client"""

    def start_socket_server(self):
        """Starts the server and makes it listen on the specifed ip and port.

        :return: A list containing the host ip and the port that the applicaition
            is listening on
        :rtype: list
        """
        address = (self.__HOST, self.__PORT)
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind(address)
        self.__server.listen()

    def stop_socket_server(self):
        """Stops the server from listening on the IP and port.
        """
        self.__server.shutdown(socket.SHUT_RDWR)
        self.__server.close()

    def wait_for_connection(self):
        """Wait for and Agent Pi to connect to the server and assigns it to
        private variable.

        :return: A list containing the Agent Pi's IP and port that is being used
            to communicate
        :rtype: list
        """
        self.__client, address = self.__server.accept()
        return address

    def wait_for_instruction(self):
        """Wait for the Agent Pi to indicate what it would like to do.

        :return: The message that was sent by the Agent Pi
        :rtype: string
        """
        data = self.__client.recv(4096)
        message = data.decode()
        return message

    def login(self):
        """Authenticates user via the Flask APi.\n
        This method waits for a response from the Agent Pi, sends this
        information to the Flask API and returns the response to the Agent Pi
        after encoding it.
        """

        # Getting message from Agent Pi
        data = self.__client.recv(4096)
        message = json.loads(data.decode())

        try:
            # Sending login info to API
            api_response = requests.post(
                'http://localhost:5000/api/login',
                json = message).text
        except :
            # If connection to API fails then senda a generic error message
            api_response = json.dumps({
                "user": None,
                "message": {
                    "server": ["A server error occured."]
                }})

        # Returning response to Agent Pi
        self.__client.sendall(api_response.encode())

    def unlock_car(self):
        """Unlocks a car via the Flask API.
        """
        pass

    def return_car(self):
        """Returns a car via the Flask API.
        """
        pass
