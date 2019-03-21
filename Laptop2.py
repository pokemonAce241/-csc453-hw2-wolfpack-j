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
#This is the main loop of the program. This is resposible for recieving the data from the arduino and producing the proper output
#based on parameters provided by the meassage header sent with the data
def loop():
        while True:
                message_id = none
                while (Data.availabe() > 0):
                    byte = Data.read() 
#This variable extracts the message id that is 8 bits. This determines wiether or not the loop continues to extract data. Once all
#data is sent the message_id should be a recieved message which is send to the socket after the while loop is over.
                    message_id = byte
#The following procedures extract the message, output type,message size, and end of file information that is needed.

#The specification extracts the next part of the message header after the messageid.
                    specification = Data.read()
                    spec = int(specification,2)
                
#This is a 1 bit output type that informs the program weither to print the output or write it to a file.                
                    result_type = spec&type_mask                   
                    result_type = result_type>>7

#This is a 1 bit that describes weither this message is the end of a file. It is important for when the output a file since this
#tells the program that this is the end of the file so that the program can properly close the current file and open up a new
#file in case the user wants to continue sending output to a file.
                    end_file = spec&file_end_mask
                    end_file = end_file<<1
                    end_file = end_file>>7
                
#The final part is a 5 bit section that describes the msg size of the payload attached to the message. This allows the program to
#properly extract the payload to send to output without risk of leaving any data out.
                    message_size = spec&message_size_mask

#Taking the message size, this loop goes through the payload and either prints the payload to the console window 
#or write the payload to a file depending on the output type.
                    for x in range(message_size):
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

#This is resposible for closing the tcp connection gracefully so that their are no error.
 clean_up()       

#This method establishes a tcp connection with the raspberrypi
def connect():
    global send_socket, HOST, PORT
    # establish a connection to the remote server
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_socket.connect((HOST, PORT))
        
# Closes the send_socket
def clean_up():
        send_socket.close()  

       

