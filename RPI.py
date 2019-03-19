import RPi.GPIO as GPIO
import time
import signal
import sys

def signal_handler(sig, frame):
	GPIO.cleanup()
	sys.exit(0)


def main():
	global id
	signal.signal(signal.SIGINT, signal_handler)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(26,GPIO.OUT)
	id = 0
	
	# get a byte and send it
	while(True):
		sendByte('c');


def sendByte(m):
	i = ord(m) # Get the integer value of the byte
	messageBin = "{0:8b}".format(i) # returns the string representation for the binary of the byte held by message
	
	idBin = "{0:8b}".format(id) # returns the string representation for the binary of the byte held by id

	messageToSend = idBin + messageBin

	for c in messageToSend:
		if ( c == '1' ):
			GPIO.output(26,True)
			time.sleep(0.01)
		else:
			GPIO.output(26,False)
			time.sleep(0.01)

	id++