#!/usr/bin/env python

import socket
import json
import zlib
import sys
import time

HOST, PORT = "localhost", 61209
data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server and send data
sock.connect((HOST, PORT))

# Send command
sock.sendall(data)

#~ # Receive data size from the server and shut down
#~ received_size = sock.recv(1024)
#~ print "Received size: {}".format(received_size)

# Receive data from the server and shut down
buff_received = ''
while True:
    buff = sock.recv(1024)
    if not buff: break
    buff_received += buff
received = json.loads(zlib.decompress(buff_received))

# Close
sock.close()

# Display
print "Received: {}".format(received)
#datareceived = json.loads(received)
#print datareceived[2]

# Wait
#~ time.sleep(3)


