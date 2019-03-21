import serial
import socket
import time

Data = serial.Serial('/dev/ttyACM0',9600)   

host = ''
port = 23456
send_socket = None

char_mode = True
file_mode = False

count = 0

f = open('result.txt','w')

        


int type_mask = int("10000000",2)
int file_end_mask = int("01000000",2)
int message_size_mask = int("00011111",2)


clear_file()

def main():
        connect()
        loop()

def loop():
        while (Data.availabe() > 0):
            byte = Data.read() 
            message_id = byte

            specification = Data.read()
            result_type = specification&type_mask
            result_type = result_type>>7

            end_file = specification&file_end_mask
            end_file = end_file<<1
            end_file = end_file>>7

            message_size = specification&message_size_mask

            message_size = (int)message_size
            result_type = (int)result_type

            for x in message_size:
                payload = Data.read()
                if result_type == 0:
                     Data.print(payload)   
                else:
                     if: (int)end_file == 1
                        f.close()
                     else:
                        f.write(payload)

        

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
