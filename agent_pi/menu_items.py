import getpass, json

def menu(master_pi, car_id):
    """Displays a menu that users can select from that calls other methods

    :param master_pi: The socket connection to the Master Pi
    :type master_pi: socket
    :param car_id: The id of the car
    :type car_id: string
    """
    user = "None"
    while True:
        if user == None:
            print("\nYou will need to log in to continue")
            user = login(master_pi)
        else:
            print("\n1. Unlock Car"
                + "\n2. Return Car"
                + "\n3. Logout")
            selection = input("Make selection [1-3]: ")
            if selection == "1":
                unlock_car(master_pi, car_id)
            elif selection == "2":
                return_car(master_pi, car_id)
            elif selection == "3":
                user = None
            else:
                print("Incorrect selection")

def login(master_pi):
    """Sends user credentials to the Master Pi to log in.\n
    Gets the username and password via user input, dumps these values as json,
    encodes it and sends it to the Master Pi via the TCP socket.\n
    The method then waits for a response where either an error is displayed or
    the username is returned, indicating a successful login.

    :param master_pi: The socket connection to the Master Pi
    :type master_pi: socket
    :return: The username of the logged in user
    :rtype: string
    """
    user = None

    # Indicating to Master Pi to begin login
    message = "Login"
    master_pi.sendall(message.encode())

    # Sending login credentials along with other information
    username = input("Enter username: ")
    password = getpass.getpass(prompt='Enter Password: ')
    message = json.dumps({
        "username": username,
        "password": password
    })
    master_pi.sendall(message.encode())

    # Checking if login was succesfull
    data = master_pi.recv(4096)
    response = json.loads(data.decode())
    if response['user'] is None:
        print("The following error(s) occured:")
        for error in response['message']:
            print("- " + response['message'][error][0])
    else:
        user = response['user']['username']
        print("Logged in as - " + user)

    return user

def unlock_car(master_pi, car_id):
    """Sends a message via sockets to unlock the car this Pi corresponds to.

    :param master_pi: The socket connection to the Master Pi
    :type master_pi: socket
    :param car_id: The id of the car
    :type car_id: string
    """
    pass

def return_car(master_pi, car_id):
    """Sends a message via sockets to return the car that this Pi corresponds to.

    :param master_pi: The socket connection to the Master Pi
    :type master_pi: socket
    :param car_id: The id of the car
    :type car_id: string
    """
    pass
