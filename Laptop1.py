import socket

# getting command line arguments
import sys, getopt

# for handling CTRL + C
import signal, time


# default to localhost
tcp_ip = '127.0.0.1'
tcp_port = 8080
file_name = "stdin"
fd = sys.stdin

def main():
    print("test")
    global tcp_ip, tcp_port,file_name,s,fd

    # parse the command line arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:")
    except getopt.GetoptError:
        print('GET OPT ERROR')
        return
    for opt in opts, argument in opts:
        if opt == '-i':
            tcp_ip = argument
        if opt == '-f':
            file_name = argument
        if opt == '-p':
            tcp_port = argument
            

    print("Connecting to ip: " + str(tcp_ip) + " port: " + str(tcp_port) + "\n\n ...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((tcp_ip, tcp_port))
    count = 0
    print("Connected to ip: " + tcp_ip + " port: " + TCP_PORT)
   # handle reading and sending from stdin
    if file_name == Null:
        while True:
            message = sys.stdin.read()
            s.send(message)
            print "message sent:"
    else:
        # handle reading and sending from a file
        fd = open(file_name,"r")
        message = fd.read() # returns one big string
        s.send(message)
        print "message sent"

    s.close()

# handle CTRL+C
def signal_handler(sig, frame):
    print('\nDisconnecting gracefully')
    if (s != None):
        s.close()
    if (fd != None and file_name != "stdin"):
        fd.close()
    # wait before ending the program
    time.sleep(0.5)
    sys.exit(0)
    
main()