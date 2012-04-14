##client.py
from socket import *
 
HOST = 'localhost'
PORT = 29877   #our port from before
ADDR = (HOST,PORT)
BUFSIZE = 4096
 
cli = socket( AF_INET,SOCK_STREAM)
cli.connect((ADDR))
 
data = cli.recv(BUFSIZE)
print data

cli.close()