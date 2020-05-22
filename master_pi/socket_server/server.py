import json, pickle, requests, socket
from face_recognition_util import FaceRecognitionUtil

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
    __fru = FaceRecognitionUtil()
    """Used to call all the facial recognition functions"""

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
        # Indicating to Agent Pi that the method has begun
        self.__client.sendall("OK".encode())

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

    def add_face(self):
        """Recieve an image from the Agent Pi and add it to the dataset.\n
        This method recieves the image and username from the Agent Pi, encodes it
        and adds it to the dataset. It sends an 'ok' response when the process
        has completed.
        """
        # Indicating to Agent Pi that the method has begun
        self.__client.sendall("OK".encode())

        # Recieve username and image from Agent Pi
        message = self.recieve_image_from_client()
        username = message['username']
        image = message['image']

        # Saving and encoding images
        self.__fru.add_face(username, image)
        self.__fru.encode_faces()

        # Letting Agent Pi know that the process has completed
        self.__client.send("OK".encode())

    def login_with_face(self):
        """Recieve an image from the Agent Pi and checks wether it matches a
        user in the dataset.\n
        This method recieves the image from the Agent Pi and checks wether it
        matches a user in the datset, it returns this information to the Agent
        Pi, via sockets, as a dict.
        """
        # Indicating to Agent Pi that the method has begun
        self.__client.sendall("OK".encode())

        # Recieve image from Agent Pi
        image = self.recieve_image_from_client()
        # Getting the matching user
        username = self.__fru.recognise_face(image)
        response = json.dumps({
            "username": username
        })

        self.__client.send(response.encode())

    def recieve_image_from_client(self):
        """Recieve an image from the Agent Pi via socketss.\n
        This method recieves the image from the Agent Pi in chunks as the image
        is too large to be sent in one go.

        :return: The image that has been recieved
        :rtype: numpy.ndarray
        """
        # Recieving image as a pickle, which is a very large strin and thus is
        # the data is broken up and recieved in a loop
        data = []
        recieving = True
        while recieving:
            packet = self.__client.recv(4096)
            try:
                # If the terminating string has been found in one of the pakcets
                # then stop the loop and append whatever information is in that
                # packet (besides the terminating string).
                end_index = packet.index(b"\x80\x03X\x08\x00\x00\x00ENDIMAGEq\x00.")
                data.append(packet[0:end_index])
                recieving = False
            except ValueError:
                # The terminating string is not in the packet and should be add-
                # ed to the data
                data.append(packet)

        return pickle.loads(b"".join(data))

    def change_lock_status(self):
        """Makes a call on the API to unlock or return a car.\n
        This method recieves the ID of a car, the username of the of the user
        that is sending the requet and what method is to be called.
        It then makes a request to the API to unlock or return the car
        corresponding to that ID. It then sends the response from the API to the
        Agent Pi via TCP sockets.
        """
        # Indicating to Agent Pi that the method has begun
        self.__client.sendall("OK".encode())

        # Getting message from Agent Pi
        data = self.__client.recv(4096)
        message = json.loads(data.decode())

        try:
            # Sending login info to API
            api_response = requests.post(
                'http://localhost:5000/api/' + message['method'],
                json = message).text
        except :
            # If connection to API fails then send a generic error message
            api_response = json.dumps({
                "message": "A server error occured."
            })

        # Returning response to Agent Pi
        self.__client.sendall(api_response.encode())

    def get_server(self):
        """Returns the server socket object.

        :return: The server socket
        :rtype: socket
        """
        return self.__server

    def get_client(self):
        """Returns the client socket object.

        :return: The client socket
        :rtype: socket
        """
        return self.__client
