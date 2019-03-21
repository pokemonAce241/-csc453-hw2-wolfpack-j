import serial
import socket
import time

Data = serial.Serial('/dev/ttyACM0',9600)   
host =
port = 2424



        
char byte

while (Data.availabe() > 0):
    byte = Data.read()
    Data.print(byte)
    
print(data)

