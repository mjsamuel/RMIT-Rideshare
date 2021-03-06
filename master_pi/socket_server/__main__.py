import logging

from server import Server


def main():
    """Main method to run necessary methods.\n
    This method starts a TCP socket, waits for and establishes a connection, and
    then starts the menu that awaits for commands.
    """
    # Setting logging level
    logging.basicConfig(level=logging.INFO)

    # Starting TCP socket server
    server = Server()
    server_address = server.start_socket_server()
    logging.info("Listening on {}...".format(server_address))

    try:
        # Wait for Agent Pi to connect to this server
        while True:
            logging.info("Waiting for Agent Pi to connect")
            client_address = server.wait_for_connection()
            logging.info("Connected to Agent Pi on {}".format(client_address))
            operations(server)
    except KeyboardInterrupt:
        logging.info("Server shutdown via keyboard interrupt")
    finally:
        logging.info("Goodbye")
        server.stop_socket_server()


def operations(server):
    """Menu to indicate to the server what operation the Agent Pi wants to do.

    :param server: The server object that is connected to the Agent Pi
    :type server: Server
    """
    continue_loop = True
    while continue_loop:
        logging.info("Waiting for instruction...")
        instruction = server.wait_for_instruction()

        if instruction == "Login":
            logging.info("Login called")
            server.login()
        elif instruction == "Login With Face":
            logging.info("Login with face called")
            server.login_with_face()
        elif instruction == "Login With Bluetooth":
            logging.info("Login with bluetooth called")
            server.login_with_bluetooth()
        elif instruction == "Change Lock Status":
            logging.info("Change lock status called")
            server.change_lock_status()
        elif instruction == "Change Car Location":
            logging.info("Change car location called")
            server.change_car_location()
        elif instruction == "Add Face":
            logging.info("Add face called")
            server.add_face()
        elif instruction == "Add Bluetooth":
            logging.info("Add bluetooth called")
            server.add_bluetooth()
        elif instruction == "":
            logging.warning("Agent Pi disconnected")
            continue_loop = False
        else:
            logging.info("Invalid instruction: " + instruction)


if __name__ == "__main__":
    main()
