import serial
import socket
import time
#This creates a serial connection with the Arduino
Data = serial.Serial('/dev/ttyACM0',9600)   

host = ''
port = 23456
send_socket = None

#these create the files recieves from laptop one. The count vaiable is used to allow for multiple files to be created before shutdown
count = 0
filename = count + "result.txt"
f = open(filename,'w')

        

#These masks are meant to extract the needed bits from the message sent from the arduino to recieve the needed parameters for 
#displaying the output
int type_mask = int("10000000",2)
int file_end_mask = int("01000000",2)
int message_size_mask = int("00011111",2)


#This is the main function that runs the entire program
def main():
        connect()
        loop()
#
def loop():
while true:
        message_id = none
        while (Data.availabe() > 0):
            byte = Data.read() 
            message_id = byte
#The following functions extract the message, output type,message size, and end of file information that is needed.
            specification = Data.read()
            spec = int(specification,2)
                
            result_type = spec&type_mask
            result_type = bin(result_type)
            result_type = result_type>>7

            end_file = spec&file_end_mask
            end_file = bin(end_file)
            end_file = end_file<<1
            end_file = end_file>>7

            message_size = spec&message_size_mask

            message_size = int(message_size,2)
            result_type = int(result_type, 2)
            end_flie = int(end_file,2)
#Taking the message size, this loop goes through and either prints the payload or write it to a file depending on the output type.
            for x in message_size:
                payload = Data.read()
                if result_type == 0:
                     Data.print(payload)   
                else:
                     if: end_file == 1
                        f.close()
                        count++
                        f = open(filename,'w')
                     else:
                        f.write(payload)
#sends a data recieved message once all the data has moved from the raspberrypi to laptop2
sent_socket.send(message_id)

        

#This method establishes a tcp connection with the raspberrypi
def connect():
    global send_socket, HOST, PORT
    # establish a connection to the remote server
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_socket.connect((HOST, PORT))
        
# Closes the send_socket
def clean_up():
        send_socket.close()  

       

