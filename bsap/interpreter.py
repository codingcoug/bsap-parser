"""
This file contains code that can break down a hex_str BSAP
message into its composite parts. It then prints the break
down.
"""

from PyCRC.CRCCCITT import CRCCCITT
from tabulate import tabulate
from constants import DLE, ETX, STX, POLL_FUNC, ACK_FUNC, ASK_NODATA_FUNC
from constants import NAK_FUNC, UP_ACK_FUNC, POLL_LIST


def print_errors(errors: list) -> bytearray:
    """
    Function to print errors found while dissecting message
    """
    print("ERRORS: ".join(format(x, '') for x in errors))
    return bytearray()


def dissect_message(hex_str: str, verbose: bool) -> bytearray:
    """
    Taking a string of hex numbers, parse the
    message check for errors.
    """
    # list for errors
    errors = list()
    # Separate the hex message into individual sections
    # original = int(, 16)
    bits = bytearray(hex_str)

    if ((bits[0] != bytearray(DLE)[0]) or (bits[1] != bytearray(STX)[0])):
        errors.append("Message must begin with {},{}. \
                       Began with {},{}".format(DLE, STX, bits[0], bits[1]))
        return print_errors(errors)

    # Create bytearray for crc
    crc = list()

    # Message starts correctly
    addr = bits[2]
    serial = bits[3]
    message = list()

    # Add things to the crc needed to calculate it
    crc.append(bytearray(STX)[0])
    crc.append(addr)
    crc.append(serial)

    i = 4   # Iterator through bitarray until DLE ETX combo found
    while ((bits[i] != bytearray(DLE)[0]) and
           (bits[i + 1] != bytearray(ETX)[0]) and
           (i < (len(bits) - 1))):
        # print("Index: {}, Value: {}".format(i,bits[i]))
        message.append(bits[i])
        crc.append(bits[i])
        i += 1

    if i == len(bits):
        errors.append("DLE({}), ETX({}) combo never found \
                      to end message".format(DLE, ETX))
        return print_errors(errors)

    crc.append(bits[i + 1])     # Append the ETX, not the DLE

    given_crc = [bits[i + 2], bits[i + 3]]
    byte_string = "".join(chr(x) for x in crc)
    calculated_crc = CRCCCITT().calculate(byte_string)

    # Calculate the CRC and ensure it matches the last two bytes
    if calculated_crc != (given_crc[0] << 8) | given_crc[1]:
        errors.append("Calculated CRC <{}> does not match given CRC \
                       <{}>".format(hex(calculated_crc),
                                    hex((given_crc[0] << 8) | given_crc[1])))
        return print_errors(errors)

    # Determine message type
    message_type = ""
    if message[0] == bytearray(POLL_FUNC)[0]:
        message_type = "POLL"
    elif message[0] == bytearray(ACK_FUNC)[0]:
        message_type = "ACK"
    elif message[0] == bytearray(ASK_NODATA_FUNC)[0]:
        message_type = "ASK_NODATA"
    elif message[0] == bytearray(NAK_FUNC)[0]:
        message_type = "NAK_FUNC"
    elif message[0] == bytearray(UP_ACK_FUNC)[0]:
        message_type = "UP_ACK"
    else:
        errors.append("Message type is unknown.")
        return print_errors(errors)

    type_byte = message[0]
    message_bytes = message[1:]

    # Print information?
    if verbose:
        # Print found information
        print(tabulate([["".join(format(x, '02x') for x in bits),
                         format(addr, '02x'),
                         format(serial, '02x'),
                         hex(type_byte), message_type,
                         "".join(format(x, '02x') for x in message_bytes),
                         hex(calculated_crc),
                         len(bits)]], headers=["Full Message",
                                               "Address",
                                               "Serial",
                                               "Function Code",
                                               "Type",
                                               "Message",
                                               "CRC",
                                               "Length"]))
    return bytearray(message)


if __name__ == "__main__":
    dissect_message(POLL_LIST[0], True)
    dissect_message(POLL_LIST[1], True)
