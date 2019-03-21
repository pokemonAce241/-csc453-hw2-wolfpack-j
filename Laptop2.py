import serial
import socket
import time

Data = serial.Serial('/dev/ttyACM0',9600)   

host =
port = 12345
send_socket = None



        
char byte

while (Data.availabe() > 0):
    byte = Data.read()
    Data.print(byte)
    
print(data)


def connect():
    global send_socket, HOST, PORT
    # establish a connection to the remote server
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_socket.connect((HOST, PORT))
        
# Closes the send_socket
def clean_up():
    if (send_socket):
        send_socket.close()      

