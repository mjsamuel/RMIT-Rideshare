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
            user = login_menu(client)
        else:
            print("\nLogged in as - " + user)
            print("1. Unlock Car"
                + "\n2. Return Car"
                + "\n3. Setup facial recognition login"
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
                print("Invalid selection")

def login_menu(client):
    """Displays a menu that users can select from to choose there login option

    :param client: The socket connection to the Master Pi
    :type client: Client
    :return: The username of the logged in user if successful
    :rtype: string
    """
    user = None
    print("1. Login via text"
        + "\n2. Login via facial recognition")
    selection = input("Make selection [1-2]: ")
    if selection == "1":
        user = login_via_text(client)
    elif selection == "2":
        user = login_via_face(client)
    else:
        print("Invalid selection")
    return user

def login_via_text(client):
    """Gets user credentials to log in user.\n
    Gets the username and password via user input, passes these values to the
    client.\n
    The method then recieves a response from the client where either an error is
    displayed or the username is returned, indicating a successful login.

    :param client: The socket connection to the Master Pi
    :type client: Client
    :return: The username of the logged in user if successful
    :rtype: string
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

    return user

def login_via_face(client):
    """Authenticates the user via their face to log in.\n
    Gets the path to an image of the user's face, creates and image object and
    sends it to the Master Pi. If recognised by the Master Pi as a user than the
    username is returned.

    :param client: The socket connection to the Master Pi
    :type client: Client
    :return: The username of the logged in user if successful
    :rtype: string
    """
    user = None

    # Getting to the path to the image of the user's face
    img_path = input(
        "Enter path to an image of your face: "
        +  str(os.path.expanduser('~'))
        + "/")
    path = os.path.join(os.path.expanduser('~'), img_path)

    image = cv2.imread(path)
    if image is None:
        print("ERROR: Image does not exist")
    else:
        print("Processing...")
        # Checking for successful login
        response = client.login_via_face(image)
        if response['username'] is None:
            print("Unsuccessful Login.")
        else:
            user = response['username']

    return user

def add_face(client, username):
    """Adds a logged in user's face to the Master Pi's dataset.\n
    Gets the path to an image of the user's face, creates and image object and
    sends it to the Master Pi for it to be stored

    :param client: The socket connection to the Master Pi
    :type client: Client
    :param username: The username of the user who's face is being registered
    :type username: string
    """
    # Getting to the path to the image of the user's face
    img_path = input(
        "Enter path to an image of your face: "
        +  str(os.path.expanduser('~'))
        + "/")
    path = os.path.join(os.path.expanduser('~'), img_path)

    image = cv2.imread(path)
    if image is None:
        print("ERROR: Image does not exist")
    else:
        print("Processing image and adding to dataset...")
        client.add_face(username, image)
        print("Finished!")

def unlock_car(client, car_id):
    """Sends a message via sockets to unlock the car this Pi corresponds to.

    :param client: The socket connection to the Master Pi
    :type client: Client
    :param car_id: The ID of the car that this Agent Pi corresponds to
    :type car_id: string
    """

    client.unlock_car(car_id)
    response = client.unlock_car(car_id)

    if response['unlock_car'] is None:
        print("The following error(s) occured:")
        for error in response['message']:
            print("- " + response['message'][error][0])
    else:
        unlock_car = response['unlock_car']['car_id']
    return unlock_car

def return_car(client, car_id):
    """Sends a message via sockets to return the car that this Pi corresponds to.

    :param client: The socket connection to the Master Pi
    :type client: Client
    :param car_id: The ID of the car that this Agent Pi corresponds to
    :type car_id: string
    """
    return_car = None

    client.return_car(car_id)
    response = client.return_car(car_id)

    if response['return_car'] is None:
        print("The following error(s) occured:")
        for error in response['message']:
            print("- " + response['message'][error][0])
            print("Car has failed to be returned")
    else:
        return_car = response['return_car']['car_id']
        print("Car has been returned !")

    return return_car
