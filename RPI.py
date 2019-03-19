import RPi.GPIO as GPIO
import time
import signal
import sys

def signal_handler(sig, frame):
	GPIO.cleanup()
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.OUT)

while (True) :
	GPIO.output(26,True)
	time.sleep(0.01)
	GPIO.output(26,False)
	time.sleep(0.01)


message = # Byte From tcp connection

id = 0;
message_header = []

for c in messageToSend:
	if ( c == 0 ):
		
	else:
		


def intTobits(n):
	return [1 if digit=='1' else 0 for digit in bin(n)[2:]]
