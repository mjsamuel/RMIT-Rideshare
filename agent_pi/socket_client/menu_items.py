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
        if user is None:
            print("\nYou will need to log in to continue")
            user = login_menu(client)
        else:
            print("\nLogged in as - " + user)
            print("1. Unlock Car"
                  + "\n2. Return Car"
                  + "\n3. Set Location"
                  + "\n4. Setup facial recognition login"
                  + "\n5. Logout")
            selection = input("Make selection [1-5]: ")
            if selection == "1":
                change_lock_status(client, user, car_id, "unlock")
            elif selection == "2":
                change_lock_status(client, user, car_id, "return")
            elif selection == "3":
                set_location(client, car_id)
            elif selection == "4":
                add_face(client, user)
            elif selection == "5":
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
        + str(os.path.expanduser('~'))
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
        + str(os.path.expanduser('~'))
        + "/")
    path = os.path.join(os.path.expanduser('~'), img_path)

    image = cv2.imread(path)
    if image is None:
        print("ERROR: Image does not exist")
    else:
        print("Processing image and adding to dataset...")
        client.add_face(username, image)
        print("Finished!")


def change_lock_status(client, username, car_id, method):
    """Sends a message via sockets to unlock or return the car this Pi corresponds to.

    :param client: The socket connection to the Master Pi
    :type client: Client
    :param username: The username of the user who is currently logged in
    :type username: string
    :param car_id: The ID of the car that this Agent Pi corresponds to
    :type car_id: string
    :param method: String to indicate wether the user wants to return or unlock
    :type method: string
    """
    response = client.change_lock_status(username, car_id, method)
    print(response)


def set_location(client, car_id):
    """Sends a message via sockets to change location of the car this Pi corresponds to.

    :param client: The socket connection to the Master Pi
    :type client: Client
    :param car_id: The ID of the car that this Agent Pi corresponds to
    :type car_id: string
    """

    # Get exact location of car from engineer
    print("Please provide exact longitude and latitude for car.")
    print("Note: 6 digits of precision are required.")
    print("Example: -37.790162,145.001738")

    location = input("Location: ")
    if location is None:
        print("ERROR: No location specified.")
    elif validate_location(location):
        print("Updating cars location now...")
        # Update car location method
        response = client.set_location(car_id, location)
        print(response)
        print("Finished!")
    else:
        print("ERROR: Invalid location provided.")


def validate_location(loc):
    """Validates the users location input.

    :param loc: The location to be validated
    :type loc: String
    :return: True if input is valid
    :rtype: boolean
    """
    # First check loc can be split into long and lat
    try:
        result = loc.split(',', 1)
    except:
        return False

    # Now check long/lat can be converted to float
    try:
        float(result[0])
        float(result[1])
    except:
        return False

    # If passes both, can assume valid location
    return True
