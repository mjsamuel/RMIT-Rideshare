import getpass

def menu(client):
    """Displays a menu that users can select from that calls other methods

    :param client: The socket connection to the Master Pi
    :type client: Client
    """
    user = None
    while True:
        if user == None:
            print("\nYou will need to log in to continue")
            user = login(client)
        else:
            print("\n1. Unlock Car"
                + "\n2. Return Car"
                + "\n3. Logout")
            selection = input("Make selection [1-3]: ")
            if selection == "1":
                unlock_car(client, car_id)
            elif selection == "2":
                return_car(client, car_id)
            elif selection == "3":
                user = None
            else:
                print("Incorrect selection")

def login(client):
    """Gets user credentials to log in user.\n
    Gets the username and password via user input, passes these values to the
    client.\n
    The method then recieves a response from the client where either an error is
    displayed or the username is returned, indicating a successful login.

    :param client: The socket connection to the Master Pi
    :type client: Client
    """
    user = None

    username = input("Enter username: ")
    password = getpass.getpass(prompt='Enter Password: ')
    response = client.login(username, password)
    if response['user'] is None:
        print("The following error(s) occured:")
        for error in response['message']:
            print("- " + response['message'][error][0])
    else:
        user = response['user']['username']
        print("Logged in as - " + user)

    return user

def unlock_car(client):
    """Sends a message via sockets to unlock the car this Pi corresponds to.

    :param client: The socket connection to the Master Pi
    :type client: Client
    """
    pass

def return_car(client):
    """Sends a message via sockets to return the car that this Pi corresponds to.

    :param client: The socket connection to the Master Pi
    :type client: Client
    """
    pass
