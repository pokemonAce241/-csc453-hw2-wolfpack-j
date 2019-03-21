import RPi.GPIO as GPIO
import time
import datetime
import signal
import sys

import socket
import select

# the size of the messages to receive from Laptop1 (this also serves as the
# size of file messages that we will send through the LED)
CHUNK_SIZE = 64

# a blank string means 'localhost' for sockets
LOCALHOST = ''

# the port that Laptop1 will connect on
LAPTOP1_CONN_PORT = 12345

# the port that Laptop2 will connect on
LAPTOP2_CONN_PORT = 23456

# the time in seconds that a bit should be sent within
TIME_PER_BIT = 0.060

START_PATTERN_TIME = 0.55

# the socket that Laptop1 will connect through
listen_socket_1 = None

listen_socket_2 = None

# the socket that Laptop1 to send data to
data_socket = None

# the socket that Laptop2 will send ACKs to
ack_socket = None

# the current message id that we're using
current_msg_id = 0


def main():
    # setup GPIO pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)

    listen(LAPTOP2_CONN_PORT)

    transmit_loop()
 #   send_message("hello world")
# Listens for a connection from Laptop1 and then a connection from Laptop2
def listen():
    global LOCALHOST, LAPTOP1_CONN_PORT, LAPTOP2_CONN_PORT, listen_socket_1, listen_socket_2, data_socket, ack_socket
    # start listening for Laptop1 connection
    listen_socket_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket_1.bind((LOCALHOST, LAPTOP1_CONN_PORT))
    listen_socket_1.listen()
    data_socket, addr = listen_socket_1.accept()

    # start listening for Laptop2 connection
    # listen_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # listen_socket_2.bind((LOCALHOST, LAPTOP2_CONN_PORT))
    # listen_socket_2.listen()
    # ack_socket, addr = listen_socket_2.accept()

# Starts the loop for receiving new data that should be transmitted
# and receiving ACKs
def transmit_loop():
    # add both sockets to the list of 'files' that we're waiting for input from
    # rlist = [data_socket, ack_socket]
    rlist = [data_socket]
    wlist = []
    xlist = []

    while (rlist):
        # wait for one of the 'files' to be ready
        (rready, wready, xready) = select.select(rlist, wlist, xlist)
        # iterate through the 'files' that are ready to read
        for ready_file in rready:
            file_num = ready_file.fileno()
            # if the ready file is data_socket
            if (file_num == data_socket.fileno()):
                chunk = data_socket.recv(CHUNK_SIZE)
                while chunk:
                    print(str(datetime.datetime.now()) + ' ' + str(chunk))
                    send_message(chunk)
                    print(str(datetime.datetime.now()) + ' DONE')
                    chunk = data_socket.recv(CHUNK_SIZE)
                # TODO transmit or store the message depending on if an ACK for the last one has returned
            # else if the ready file is ack_socket
            # elif (file_num == ack_socket.fileno()):
            #     ack = ack_socket.recv(CHUNK_SIZE)
                # TODO check if the msgID in the ack matches the message that was just transmitted


# modulate the given message through the LED
def send_message(m):
    global current_msg_id
#    m = "hello world".encode('utf-8')
    # construct the binary representation of the message
    messageBin = ''
    for char in m:
        #i = ord(char) # Get the integer value of the byte
        binRepresentation = "{0:08b}".format(int(char)) # returns the string representation for the binary of the byte held by message
        messageBin += binRepresentation
        print(binRepresentation + " ")

    # construct the binary representation of the header
    idBin = "{0:08b}".format(current_msg_id) # returns the string representation for the binary of the byte held by id

    # concatenate everything together
    messageToSend = idBin + messageBin
    #testMessage = "{0:08b}".format(78) + "{0:08b}".format(255) #+ "{0:08b}".format(77)+ "{0:08b}".format(77)
    #messageToSend = testMessage
   # print("{0:08b}".format(78))
    print("Sending message")
    start_message_pattern()
    for bit in messageToSend:
        if ( bit == '1' ):
            GPIO.output(26, True)
            time.sleep(TIME_PER_BIT)
        else:
            GPIO.output(26, False)
            time.sleep(TIME_PER_BIT)
    end_message_pattern()

    current_msg_id += 1

# modulates the start pattern (on, off, on, off)
def start_message_pattern():
    GPIO.output(26, True)
    ## time.sleep(TIME_PER_BIT / 2)
    ## GPIO.output(26, False)
    ## time.sleep(TIME_PER_BIT / 2)
    ## GPIO.output(26, True)
    ## time.sleep(TIME_PER_BIT / 2)
    ## GPIO.output(26, False)
    ## time.sleep(TIME_PER_BIT / 2)
    time.sleep(START_PATTERN_TIME)

# modulates the end pattern (off, on, off, on)
def end_message_pattern():
    GPIO.output(26, False)
    ##time.sleep(TIME_PER_BIT / 2)
    ##GPIO.output(26, True)
    ##time.sleep(TIME_PER_BIT / 2)
    ##GPIO.output(26, False)
    ##time.sleep(TIME_PER_BIT / 2)
    ##GPIO.output(26, True)
    ##time.sleep(TIME_PER_BIT / 2)
    time.sleep(START_PATTERN_TIME)

# Cleans up the GPIO pins and closes all sockets
def clean_up():
    GPIO.cleanup()
    if (listen_socket_1):
        listen_socket_1.close()
    if (listen_socket_2):
        listen_socket_2.close()
    if (data_socket):
        data_socket.close()
    if (ack_socket):
        ack_socket.close()

# handle CTRL+C
def signal_handler(sig, frame):
    clean_up()
    print('\n\nHave a nice day!')
    time.sleep(0.1)
    sys.exit(0)

if __name__ == '__main__':
    try:
        # register the signal handler
        signal.signal(signal.SIGINT, signal_handler)
        main()
    except Exception as e:
        print(e)
    finally:
        clean_up()
