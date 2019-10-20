"""
bsapmodule.py

This is the main python script that will be run.
It pulls from constants.py and udpcommunication.py
to get the necessary functions

It runs as a multi-threaded program. One thread
handles listens on the proper port for UDP. The other
checks a shared queue and if there are messages
present it reads them and transmits replies.

The code is similar for both the BSAP Master and the
slave. The only difference is that the BSAP Master
initiates communication by sending an initial message.
"""

# Import functions from other .py files
from argparse import ArgumentParser
from multiprocessing import Process, Queue
import datetime
import time
from udpcommunication import transmit, receive
from constants import POLL_LIST, UDP_PORT, ACK_LIST, NAK_LIST
from constants import ASK_NODATA_LIST, ASK_NODATA_FUNC, NAK_FUNC, POLL_FUNC
from constants import UDP_IP_SLAVE, UDP_IP_MASTER, ACK_FUNC, STOP_LIST

# --------------------- GLOBALS ----------------------
# When anything but a 0 is inputted into terminal, that will become the slave
ADDRESS = 1                 # Default is SLAVE
TIMEOUT_MAX = 50000         # How long until message is LOST

THIS_MODULE_IP = None         # What IP address is this running on
OTHER_MODULE_IP = None        # What IP address is the other running on

LAST_MESSAGE_SENT = None      # Last message sent
TIMEOUT_COUNTER = 0          # How long since last message sent?

THREAD_COMMUNICATION_QUEUE = None         # Global shared queue
RECEIVE_THREAD = None	    # Global RECEIVE_THREAD for killing purposes

NUMBER_RECEIVED = 0          # How many messages have been sent
NUMBER_TRANSMITTED = 0          # how many messages have been received
MAX_NUMBER_MESSAGES = None

VERBOSE = False             # Should print output (default=False)
"""
Have any messages been received?

The following will be set as True if yes.
This indicates that communication has begun
and the kill timer for the slave is activated

As this is a simulator this is NOT normal
behaviour but is an option to allow the
program to exit if something is wrong.

It is only activated by adding a -k or --kill
to the command line when run
"""
MESSAGE_RECEIVED = False

"""
This simulator has a feature built in that
kills the slave if communication is seriously
interrupted (4 * MAX_TIMEOUT). This is
OPTIONAL and is NOT NORMAL and is simply to
ensure the slave process terminates after testing
is complete.
"""
KILL_SLAVE = False

# The following are used to calculate the
# average time between transmitted messages
TIME_1 = None
TIME_2 = None
AVERAGE_TIME = 0

# Time to wait between messages
RATE_PERIOD = 0


def finish():
    """
    Function that runs when the program is complete to
    output data
    """
    global NUMBER_TRANSMITTED
    global NUMBER_RECEIVED
    global AVERAGE_TIME
    global RECEIVE_THREAD
    # The following will print no matter what
    print("Total Messages Sent: {}".format(NUMBER_TRANSMITTED))
    # This number comes from the fact that we have processed some
    # but some may remain on the queue
    print("Total Messages Received: " +
          "{}".format(NUMBER_RECEIVED + THREAD_COMMUNICATION_QUEUE.qsize()))
    # Average time between transm`itted messages
    print("Average time between transmitted " +
          "messages: {} seconds".format(AVERAGE_TIME /
                                        1000000))
    RECEIVE_THREAD.terminate()   # Kill the receive thread
    exit(0)     # Exit successfully


def update_time():
    """
    Used to update the average time between transmitted messages
    """
    global TIME_1
    global TIME_2
    global AVERAGE_TIME
    global NUMBER_TRANSMITTED
    TIME_2 = datetime.datetime.now()
    diff = TIME_2 - TIME_1
    AVERAGE_TIME = ((AVERAGE_TIME * (NUMBER_TRANSMITTED - 1)) +
                    diff.microseconds) / NUMBER_TRANSMITTED
    TIME_1 = TIME_2


def transmit_message(message_to_send):
    """
    Function used by this document to transmit
    a message. It is a wrapper so that we can
    track how many messages have been sent and
    store what the last sent message was.
    """
    global RECEIVE_THREAD
    global VERBOSE
    global NUMBER_TRANSMITTED
    global AVERAGE_TIME
    global LAST_MESSAGE_SENT
    global TIMEOUT_COUNTER
    global TIME_1

    # If the user has defined a rate, wait to send
    if RATE_PERIOD != 0:
        # What time is it now?
        current_time = datetime.datetime.now()

        # What is the difference in time?
        diff = current_time - TIME_1

        # Has enouph time passed?
        while (diff.microseconds/1000000) < RATE_PERIOD:
            # No, so update diff
            current_time = datetime.datetime.now()
            diff = current_time - TIME_1

    # Transmit the message ONLY if the rate has passed
    # Set last message sent in case of breakdown in
    # communication
    LAST_MESSAGE_SENT = message_to_send

    # a message was sent, so reset the timeout
    TIMEOUT_COUNTER = 0

    # We have transferred another
    NUMBER_TRANSMITTED += 1

    # Update averages and TIME_1 (last time message sent)
    update_time()

    # Print if they asked for it
    if VERBOSE:
        print("\nSent: {} to {}\n".format(message_to_send, OTHER_MODULE_IP))

    # Transmit the message
    transmit(OTHER_MODULE_IP, UDP_PORT, message_to_send)

    # Check to see if we have completed the number
    if MAX_NUMBER_MESSAGES is not None:
        if NUMBER_TRANSMITTED >= MAX_NUMBER_MESSAGES:
            finish()


def receiver_thread(queue: Queue):
    """
    Thread that will receive messages
    over UDP. Will wait for packets to
    arrive and then places them in a shared
    queue for the transmitting thread to
    identify and reply to.
    """
    global VERBOSE
    while True:
        message = receive(THIS_MODULE_IP, UDP_PORT, VERBOSE)
        if VERBOSE:
            print("Received: {}".format(message))
        # Did we receive an empty message?
        if message:
            # Place the message in the shared queue
            queue.put(message)
        else:
            # Message not received, it was empty
            print("message NOT found")


def transmit_slave_thread():
    """
    This is the thread that identifies
    received messages for the slave. It
    then replies based on what the message was.
    """
    global MESSAGE_RECEIVED
    global KILL_SLAVE
    global TIMEOUT_COUNTER
    global NUMBER_RECEIVED
    while True:
        # Is something in the shared queue?
        if not THREAD_COMMUNICATION_QUEUE.empty():
            message = THREAD_COMMUNICATION_QUEUE.get()
            NUMBER_RECEIVED += 1
            # The following is only necessary if KILL_SLAVE is active
            if KILL_SLAVE:
                MESSAGE_RECEIVED = True  # A message has been received

            # THIS IS THE SLAVE
            if message[0] == bytearray(POLL_FUNC)[0]:
                # This is a POLL, return an ACK
                transmit_message(ACK_LIST[0])
            elif message[0] == bytearray(ASK_NODATA_FUNC)[0]:
                transmit_message(NAK_LIST[0])
            else:
                pass    # Slave does nothing unless asked
        else:
            # Is the option even on to kill the slave?
            if KILL_SLAVE:
                # Has communication started?
                if MESSAGE_RECEIVED:
                    # There is nothing in the queue, wait a LONG
                    # time (4 times how long the master should
                    # and then print an error
                    TIMEOUT_COUNTER += 1
                    if TIMEOUT_COUNTER >= (4 * TIMEOUT_MAX):
                        finish()
                else:
                    # Wait for communication to begin before dying
                    pass
            else:
                # No we are not killing slaves
                pass


def transmit_master_thread():
    """
    Thread that listens on the UDP port
    for the Master Node. It identifies
    received messages and then replies
    accordingly.
    """
    global TIMEOUT_COUNTER
    global NUMBER_RECEIVED
    while True:
        # Is something in the shared queue?
        if not THREAD_COMMUNICATION_QUEUE.empty():
            message = THREAD_COMMUNICATION_QUEUE.get()
            NUMBER_RECEIVED += 1
            if message[0] == bytearray(ACK_FUNC)[0]:
                # For right now, just send a POLL,
                transmit_message(ASK_NODATA_LIST[0])
            elif message[0] == bytearray(NAK_FUNC)[0]:
                transmit_message(POLL_LIST[0])
            else:
                # If master unsure what to do, poll
                transmit_message(POLL_LIST[0])
        else:
            # Nothing in the queue, count
            # to see if you need to resend the last
            # message
            TIMEOUT_COUNTER += 1
            if TIMEOUT_COUNTER >= TIMEOUT_MAX:
                if LAST_MESSAGE_SENT is not None:
                    # Timer ran out, resend last message
                    transmit_message(LAST_MESSAGE_SENT)
                else:
                    # Really shouldn't get here
                    # just in case it times out
                    transmit_message(POLL_LIST[0])


# This is the main function, as you can see it quickly
# breaks into two threads. The reason for this is so
# the receive and the send can be independant of each
# other and do not depend on precise timing.
if __name__ == "__main__":
    ARGS = ArgumentParser()
    ARGS.add_argument("-a", "--address",
                      type=int,
                      default=1,
                      required=True,
                      help="Is this the master (0) or a slave (1)?"
                      )
    ARGS.add_argument("-n", "--messageNumber",
                      type=int,
                      help="Number of messages the master will send (> 1)")
    ARGS.add_argument("-t", "--messageTimeout",
                      type=int,
                      default=50000,
                      help="How long should the master wait (in ticks) \
                            after NOT receiving a message to resend the \
                            last message? DEFAULT: 50000")
    ARGS.add_argument("-v", "--VERBOSE",
                      action='store_true',
                      help="Print detailed output")
    ARGS.add_argument("-k", "--kill",
                      action='store_true',
                      help="Activate Slave Kill Switch if communication \
                            seriously interrupted (4 * messageTimeout)"
                      )
    ARGS.add_argument("-dd", "--ddos",
                      action='store_true',
                      help="DDOS Testbench, ONLY RUN AS MASTER"
                      )
    ARGS.add_argument("-s", "--stop",
                      action='store_true',
                      help="Stop Process, ONLY RUN AS MASTER"
                      )
    ARGS.add_argument("-r", "--rate",
                      type=int,
                      help="Number of messages per Second"
                      )
    # Set up multi-threading communication queue
    THREAD_COMMUNICATION_QUEUE = Queue()

    # Handle arguments
    OPTS = ARGS.parse_args()
    # Is this the master or the slave?
    ADDRESS = OPTS.address

    # Did they provide a certain number of
    # messages they want send?
    if OPTS.messageNumber:
        MAX_NUMBER_MESSAGES = OPTS.messageNumber

    # Did they specify a timeout max?
    if OPTS.messageTimeout:
        # Yes, they did, overwrite the default
        TIMEOUT_MAX = OPTS.messageTimeout

    # Do they want a printed output?
    if OPTS.VERBOSE:
        # Yes
        VERBOSE = True

    # Are we activating automatic slave kill?
    if OPTS.kill:
        # yes
        KILL_SLAVE = True

    # Initialize TIME_1
    TIME_1 = datetime.datetime.now()

    # If they provided a rate, calculate a period
    if OPTS.rate:
        RATE_PERIOD = 1 / OPTS.rate

    # Is this the master or the slave?
    # The answer depends on the provided address
    # By default, this module is the slave
    if ADDRESS == 0:
        # Set IP addresses
        THIS_MODULE_IP = UDP_IP_MASTER
        OTHER_MODULE_IP = UDP_IP_SLAVE

        # DDOS the testbench by sending messages
        # As fast as possible
        if OPTS.ddos:
            print("DDOS Initiated...")
            # Ignore the Rate if it was set
            RATE_PERIOD = 0
            # yes
            while True:
                transmit_message(POLL_LIST[0])

            # It won't escape, but in case, exit
            exit(0)

        # Are we attempting to stop the process?
        if OPTS.stop:
            # yes
            print("Stop Process")

            # Iterate through all possible serial
            # numbers
            for x in STOP_LIST:
                transmit_message(x)

            # Terminate, we are not simulating more
            exit(0)

        # This is the master
        transmit_message(POLL_LIST[0])
        # Start the receiver thread then run the transmitter
        RECEIVE_THREAD = Process(target=receiver_thread,
                                 args=[THREAD_COMMUNICATION_QUEUE])
        RECEIVE_THREAD.start()          # Start the second thread
        transmit_master_thread()        # Start the transmitter thread
        # Wait for RECEIVE_THREAD to finish
        RECEIVE_THREAD.join()
    else:
        # Set IP addresses
        THIS_MODULE_IP = UDP_IP_SLAVE
        OTHER_MODULE_IP = UDP_IP_MASTER
        # This is the slave
        RECEIVE_THREAD = Process(target=receiver_thread,
                                 args=[THREAD_COMMUNICATION_QUEUE])
        RECEIVE_THREAD.start()       # Start the second thread
        transmit_slave_thread()      # Start the transmitter thread
        # Wait for RECEIVE_THREAD to finish
        RECEIVE_THREAD.join()
