import json, logging, requests, socket

HOST = ""
PORT = 65000
ADDRESS = (HOST, PORT)

logging.basicConfig(level=logging.INFO)

def main():
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
    continue_loop = True
    while continue_loop:
        logging.info("Waiting for instruction...")

        data = agent_pi.recv(4096)
        message = data.decode()
        if message == "Login":
            log_in(agent_pi)
        elif message == "Unlock":
            unlock_car(agent_pi)
        elif message == "Return":
            return_car(agent_pi)
        else:
            logging.info("Agent Pi Disconnected")
            continue_loop = False

def log_in(agent_pi):
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
    pass

def return_car(agent_pi):
    pass

if __name__ == "__main__":
    main()
