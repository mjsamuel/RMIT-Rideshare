import argparse, socket

from menu_items import menu
from text_helper import *

def main():
    """Main method to run necessary methods.\n
    This method reads the command line arguments for the IP of the master pi and
    the ID of the car, creates a socket connection and starts the main menu
    """
    master_pi_ip, car_id = parse_arguments()

    print(COLOUR_GREEN + LOGO + COLOUR_END)
    try:
        master_pi = connect_to_mp(master_pi_ip)
        print("Connected to Master Pi")
        menu(master_pi, car_id)
    except ConnectionRefusedError:
        print("Failed to connect to Master Pi\n")
    except KeyboardInterrupt:
        master_pi.close()
    except Exception as e:
        print(e)
        master_pi.close()
    finally:
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

def connect_to_mp(host):
    """Creates and returns a TCP socket connection to the Master Pi

    :param host: The Master Pi's IP address
    :type host: string
    :return: A socket connection to the Master Pi
    :rtype: socket
    """
    port = 65000
    address = (host, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(address)
    return s

if __name__ == "__main__":
    main()
