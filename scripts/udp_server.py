#!/usr/bin/env python3

import socket 
# UDP Server
# NOTE: use netcat for communicating with UDP server
# nc -u 127.0.0.1 5500

localIP = "127.0.0.1"
localPort = 5500

bufferSize = 65535 # MAX 

# create UDP socket endpoint.
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# bind IP address and port, so other devices in the network
# can send data to the socket endpoint.
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# Listen for incoming datagrams
while 1:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1][0]
    port = bytesAddressPair[1][1]

    print("Message %s from client [%s:%d]" %(message, address, port))

    print("Testing .. TABs")
