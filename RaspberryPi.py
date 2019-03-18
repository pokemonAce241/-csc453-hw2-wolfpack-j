import socket

import RPi.GPIO as GPIO
import time

broker = "broker.hivemq.com"
broker = "iot.eclispe.org"

# Sets up the variou sparts o fthe Raspberry Pi that will be used to turn on and off the LED
GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.OUT)

# Initialize each of hte outputs to false to esnure the LED's start out as off
GPIO.output(5,False)

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connection address:', addr
while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print "received data:", data
    conn.send(data)  # echo
conn.close()
