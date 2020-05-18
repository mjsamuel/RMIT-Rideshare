import cv2, getpass, os

def menu(client, car_id):
    """Displays a menu that users can select from that calls other methods

    :param client: The socket connection to the Master Pi
    :type client: Client
    :param car_id: The ID of the car that this Agent Pi corresponds to
    :type car_id: string
    """
    user = None
    while True:
        if user == None:
            print("\nYou will need to log in to continue")
            user = login(client)
        else:
            print("\n1. Unlock Car"
                + "\n2. Return Car"
                + "\n3. Setup face recognition login"
                + "\n4. Logout")
            selection = input("Make selection [1-4]: ")
            if selection == "1":
                unlock_car(client, car_id)
            elif selection == "2":
                return_car(client, car_id)
            elif selection == "3":
                add_face(client, user)
            elif selection == "4":
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

def unlock_car(client, car_id):
    """Sends a message via sockets to unlock the car this Pi corresponds to.

    :param client: The socket connection to the Master Pi
    :type client: Client
    :param car_id: The ID of the car that this Agent Pi corresponds to
    :type car_id: string
    """
    pass

def return_car(client, car_id):
    """Sends a message via sockets to return the car that this Pi corresponds to.

    :param client: The socket connection to the Master Pi
    :type client: Client
    :param car_id: The ID of the car that this Agent Pi corresponds to
    :type car_id: string
    """
    pass

def add_face(client, username):
    img_path = input(
        "Enter path to an image of your face: "
        +  str(os.path.expanduser('~'))
        + "/")

    path = os.path.join(os.path.expanduser('~'), img_path)
    print(path)

    image = cv2.imread(path)
    if image is None:
        print("ERROR: Image does not exist")
    else:
        print("Adding image to dataset")
        client.add_face(username, image)
        print("Finished")
