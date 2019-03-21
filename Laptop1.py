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
PORT = 12345

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
        if (opt == '-i'):
            HOST = arg

    connect()

    curses.wrapper(input_loop)

# Connects to the HOST and PORT
def connect():
    global send_socket, HOST, PORT
    # establish a connection to the remote server
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_socket.connect((HOST, PORT))

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
                send_file_to_rpi(file_path)
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
                send_to_rpi(key)

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

# Sends the given string to the RPI
def send_to_rpi(data):
    byte_representation = data.encode('utf-8')
    send_socket.sendall(byte_representation)

# Sends the file with the given path to the RPI
def send_file_to_rpi(file_path):
    with open(file_path, 'rb') as f:
        send_socket.sendfile(f, 0)

# Closes the send_socket
def clean_up():
    if (send_socket):
        send_socket.close()

# handle CTRL+C
def signal_handler(sig, frame):
    clean_up()
    print('\n\nHave a nice day!')
    time.sleep(0.1)
    sys.exit(0)


if __name__ == '__main__':
    # register the signal handler
    signal.signal(signal.SIGINT, signal_handler)
    main()
