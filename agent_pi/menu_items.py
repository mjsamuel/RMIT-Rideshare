import getpass, json

def menu(master_pi, car_id):
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
                unlock_car(master_pi)
            elif selection == "2":
                return_car(master_pi)
            elif selection == "3":
                user = None
            else:
                print("Incorrect selection")

def login(master_pi):
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

def unlock_car(master_pi):
    pass

def return_car(master_pi):
    pass
