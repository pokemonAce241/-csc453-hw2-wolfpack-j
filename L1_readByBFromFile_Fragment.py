# Codes fragments for reading in file as b

f = open(filename, 'rb+')
buffer = f.read()
#send buffer byte by byte
for bytes in buffer:
	...
