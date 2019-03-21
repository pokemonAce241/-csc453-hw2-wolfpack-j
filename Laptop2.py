import serial
import socket
import time

Data = serial.Serial('/dev/ttyACM0',9600)   

host = ''
port = 12345
send_socket = None

f = open('result.txt','w')

        
char byte


clear_file()
while (Data.availabe() > 0):
    byte = Data.read()
    write_to_file(byte)
    Data.print(byte)
    
print(data)

def send_file_to_rpi(file_path):
    with open(file_path, 'w') as f:
        send_socket.sendfile(f, 0)


def connect():
    global send_socket, HOST, PORT
    # establish a connection to the remote server
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_socket.connect((HOST, PORT))
        
# Closes the send_socket
def clean_up():
    if (send_socket):
        send_socket.close()  

def write_to_file(byteChar)
        f.write(byteChar)
        
def clear_file()
      f.seek(0)
      f.truncate()
