import cv2, json, pickle, os, socket, sys

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
        :return: A dictionary containing the response from the Master Pi
        :rtype: dict
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

        # Returning response from Master Pi
        data = self.__server.recv(4096)
        response = json.loads(data.decode())
        return response

    def login_via_face(self, image):
        """Sends an image to the Master Pi to authenticate a user.
        \nThe image is pickled and sent via the socket. As the data is too large
        for the buffer size a terminating string is added to the end to indicate
        that the image has finished being sent.\n
        The client then waits for a response from the Master Pi of wether the
        login was successful.

        :param image: The omage of the user's face to be sent
        :type image: numpy.ndarray
        :return: A dictionary containing the response from the Master Pi
        :rtype: dict
        """
        message = "Login With Face"
        self.__server.sendall(message.encode())

        # Sending piickle to Master Pi
        self.__server.send(pickle.dumps(image))
        # Since the pickled image is too large for it to be sent in one go, it
        # has to be recieved in parts and so a terminating string is added to
        # indicate that the image has finished being sent
        self.__server.send(b'\x80\x03X\x08\x00\x00\x00ENDIMAGEq\x00.')

        # Wait for Master Pi to send back which user it has identified
        data = self.__server.recv(4096)
        response = json.loads(data.decode())
        return response

    def add_face(self, username, image):
        """Sends an image and username to the Master Pi to register a users face.
        \nThe image and username are pickled and sent via the socket. As the
        data is too large for the buffer size a terminating string is added to
        the end to indicate that the image has finished being sent.\n
        The client then waits for an 'ok' response once the Master Pi has
        finished processing and saving the image.

        :param username: The user's usernmae
        :type username: string
        :param image: The omage of the user's face to be sent
        :type image: numpy.ndarray
        """
        # Indicating to Master Pi to add face
        message = "Add Face"
        self.__server.sendall(message.encode())

        # Create pickle string of username and image
        message = pickle.dumps({
            "username": username,
            "image": image
        })

        # Sending piickle to Master Pi
        self.__server.send(message)
        # Since the pickled image is too large for it to be sent in one go, it
        # has to be recieved in parts and so a terminating string is added to
        # indicate that the image has finished being sent
        self.__server.send(b'\x80\x03X\x08\x00\x00\x00ENDIMAGEq\x00.')

        # Wait for Master Pi to indicate that the image has been saved and
        # encoded
        data = self.__server.recv(4096)

    def get_server(self):
        """Gets the Master Pi server that the Agent Pi is connected to.

        :return: Master Pi socket object
        :rtype: socket
        """
        return self.__server
