import json, logging, requests, socket

HOST = ""
PORT = 65000
ADDRESS = (HOST, PORT)

logging.basicConfig(level=logging.INFO)

def main():
    """Main method to run necessary methods.\n
    This method starts a TCP socket, waits for and establishes a connection, and
    then starts the menu that awaits for commands.
    """
    master_pi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    master_pi.bind(ADDRESS)
    master_pi.listen()
    logging.info("Listening on {}".format(ADDRESS))

    try:
        while True:
            logging.info("Waiting for connection...")
            agent_pi, address = master_pi.accept()
            logging.info("Connected to Agent Pi {}".format(address))
            menu(agent_pi)
    except (KeyboardInterrupt, json.decoder.JSONDecodeError):
        logging.info("Shutting down socket")
        master_pi.shutdown(socket.SHUT_RDWR)
        master_pi.close()

def menu(agent_pi):
    """Menu to indicate what operation the Agent Pi wants to do.

    :param agent_pi: The socket connection to the Agent Pi
    :type agent_pi: socket
    """
    continue_loop = True
    while continue_loop:
        logging.info("Waiting for instruction...")

        data = agent_pi.recv(4096)
        message = data.decode()
        if message == "Login":
            login(agent_pi)
        elif message == "Unlock":
            unlock_car(agent_pi)
        elif message == "Return":
            return_car(agent_pi)
        else:
            logging.info("Agent Pi Disconnected")
            continue_loop = False

def login(agent_pi):
    """Authenticates user via the Flask APi.\n
    This method waits for a response from the Agent Pi, sends this information
    to the Flask API and returns the response to the Agent Pi after encoding it.

    :param agent_pi: The socket connection to the Agent Pi
    :type agent_pi: socket
    """
    logging.info("Login called")

    # Getting message from Agent Pi
    data = agent_pi.recv(4096)
    message = json.loads(data.decode())

    # Sending login info to API
    api_response = requests.post(
        'http://localhost:5000/api/login',
        json = message
    )

    # Returning response to Agent Pi
    agent_pi.sendall(api_response.text.encode())

def unlock_car(agent_pi):
    """Unlocks a car via the Flask API.

    :param agent_pi: The socket connection to the Agent Pi
    :type agent_pi: socket
    """
    pass

def return_car(agent_pi):
    """Returns a car via the Flask API.

    :param agent_pi: The socket connection to the Agent Pi
    :type agent_pi: socket
    """
    pass

if __name__ == "__main__":
    main()
