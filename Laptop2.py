import socket

# getting command line arguments
import sys, getopt

# for handling CTRL + C
import signal, time

import curses

import string

# a set of the characters that are allowed in file paths (a-z A-Z 0-9 . _ - /)
ALLOWED_CHARS_IN_FILE_PATH = set(string.ascii_lowercase + string.ascii_uppercase + string.digits + '._-/')

# the host to listen on (blank for localhost)
HOST = ''
# the port to either listen on or connect to
PORT = 8000

listen_socket = None

send_socket = None

def main():
    global HOST

    # parse the command line arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:')
    except getopt.GetoptError:
        print('usage: Laptop1.py -i <hostname>')
        sys.exit(2)

    for opt, arg in opts:
        if (opt == '-c'):
            HOST = arg
            # connect(arg)

    curses.wrapper(input_loop)

def input_loop(win):
    win.nodelay(False)

    display_description(win)

    file_mode = False
    file_path = ''

    while True:
        key = win.getkey()

        # if it's file mode
        if (file_mode):
            # if the user presses the "Insert" key
            if (key == 'KEY_IC'):
                # exit file mode
                file_mode = False
                display_description(win)
            # else if the user presses the "Backspace" key
            elif (key == 'KEY_BACKSPACE'):
                # take off the last letter of the file path
                file_path = file_path[:-1]
                # redisplay the correct file path
                display_file_instructions(win, file_path)
            # else if the user types an acceptable character
            elif (is_valid_file_path_char(key)):
                win.addstr(key)
                file_path += key
            # else if the user presses the "Enter" key
            elif (key == '\n'):
                # TODO read in the file with the given name
                # TODO send the file over the TCP connection
                # exit file mode
                file_mode = False
                display_description(win)
        # else you're just processing typed text to transmit
        else:
            # if the user presses the "Insert" key
            if (key == 'KEY_IC'):
                # enter file mode
                file_mode = True
                file_path = ''
                display_file_instructions(win, file_path)
            # else if the user presses the "Delete" key
            elif (key == 'KEY_DC'):
                display_description(win)
            else:
                win.addstr(key)
                # TODO send the character over the TCP connection

def display_description(win):
    win.clear()
    win.addstr('In this window you can enter text that is immediately transmitted.\n')
    win.addstr('Press the "Delete" key to clear the text you have typed so far.\n')
    win.addstr('Press the "Insert" key to enter file mode.\nThis will allow you to enter the path to a file to transmit.\n')
    win.addstr('Enter text: ')

def display_file_instructions(win, path):
    win.clear()
    win.addstr('You can now enter the path to a file to transmit. The valid characters for a file path are: a-z A-Z 0-9 . _ - /.\n')
    win.addstr('Press the "Insert" key to go back to text mode.\n')
    win.addstr('Enter a file path: ' + path)

def is_valid_file_path_char(key):
    return len(key) == 1 and set(key).issubset(ALLOWED_CHARS_IN_FILE_PATH)

# Starts the chat loop which continuously waits for either
# local input or remote ouptut from the given connection;
#
# @param {socket} conn the connection to send message to and
#   receive messages from
def send_to_rpi(conn, data):
    conn.sendall(data)

# Connects to the given host;
#
# @param {string} hostname the host to connect to
def connect(hostname):
    global send_socket, PORT
    # establish a connection to the remote server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_socket = sock
    sock.connect( (hostname, PORT) )

# Closes any sockets that were opened;
def clean_up():
    if (send_socket):
        send_socket.close()

# handle CTRL+C
def signal_handler(sig, frame):
    clean_up()
    print('\n\nHave a nice day!')
    time.sleep(0.5)
    sys.exit(0)


if __name__ == '__main__':
    # register the signal handler
    signal.signal(signal.SIGINT, signal_handler)
    main()

