import argparse

from client import Client
from menu_items import menu
from text_helper import *

def main():
    """Main method to run necessary methods.\n
    This method reads the command line arguments for the IP of the master pi and
    the ID of the car, creates a client object that creates a connection to the
    Master Pi based on the IP and starts the main menu.
    """
    ip, car_id = parse_arguments()
    print(COLOUR_GREEN + LOGO + COLOUR_END)
    client = Client(ip, car_id)
    try:
        client.connect_to_server()
        print("Connected to Master Pi")
        menu(client, car_id)
    except ConnectionRefusedError:
        print("Failed to connect to Master Pi\n")
    except KeyboardInterrupt:
        pass
    finally:
        client.disconnect_from_server()
        print("Goodbye.")

def parse_arguments():
    """Parses the Master Pi IP and car ID from the command line arguments.\n
    Creates a parse object, specifies what arguments are required and checks to
    make sure that they are present.

    :return: A list containing the IP of the master pi and the car ID
    :rtype: list
    """
    parser = argparse.ArgumentParser(
        description='Car interface to connect to RMIT Rideshare Master Pi')
    parser.add_argument(
        'master_pi_ip',
        type=str,
        help='The IP of the Master Pi')
    parser.add_argument(
        'car_id',
        type=str,
        help='The ID of the car this Agent Pi corresponds to')

    args = parser.parse_args()
    return (args.master_pi_ip, args.car_id)

if __name__ == "__main__":
    main()
