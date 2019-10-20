"""
This file includes the functions necessary to transmit
and receive UDP packets
"""
import socket

# Read in constants file
from constants import BUFF_SIZE
from interpreter import dissect_message


def receive(ip_addr: str, port: int, verbose: bool):
    """
    Function that receives a messages over
    UDP on a given port/ip address combo.
    """
    # Set the socket up to run across internet and to use UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind our socket to the passed in IP and port num
    sock.bind((ip_addr, port))

    # Recieve the data as well as the address that sent it
    data_received, addr = sock.recvfrom(BUFF_SIZE)

    # data_received = data.decode("utf-8") # Decode the bytes string
    if verbose:
        print("Received message: {} from: {}".format(data_received, addr))

    message = dissect_message(data_received, verbose)  # Dissect the message
    return message


def transmit(ip_address, port, message):
    """
    Function to transmit a message over
    UDP to a given ip address/port pair.
    """
    # Specify the message to be sent
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP

    # Send the message to the specified IP and port
    sock.sendto(message, (ip_address, port))
    # print("Message sent")
