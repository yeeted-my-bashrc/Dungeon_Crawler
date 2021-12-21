#!/usr/bin/python3
#THIS ALLOWS YOU TO RUN AS ./filename.py
#give permission by: chmod +x filename.py
import socket
import threading

running =True;

#create server socket
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#binds socket to a host and port
s.bind((socket.gethostname(), 50000))
print("bound to address ", s.getsockname())

#socket listens for up to 5 connections
s.listen(5)

def send(conn,msg):
  #this encodes msg and sets a header which represents msg length, I think
  msg = f'hello world from server'.encode()
  msg = bytes(f"{len(msg):<{headerSize}}",'utf-8')+msg
  conn.send(msg)

headerSize=10
msglen=100

def receive(conn, addr):
  global headerSize,msglen
  while running:
    msg_buffer = b''
    new_msg = True
    while True:

      #Now i know exactly how this works. I would like to do google meet to explain it.
      if (len(msg_buffer) < msglen):
        msg = conn.recv(1024)
        msg_buffer += msg
        print(msg_buffer)

      if new_msg:
        msglen = int(msg_buffer[:headerSize])
        new_msg = False

      #this is when it knows it received the whole message, and then decodes it
      if len(msg_buffer)-headerSize >= msglen:
        decoded_msg = msg_buffer[headerSize:headerSize + msglen].decode()
        print(headerSize,msglen,"full message: ",decoded_msg)

        new_msg = True
        msg_buffer = msg_buffer[headerSize+msglen:]

while running:
  conn, addr = s.accept()
  thread = threading.Thread(target = receive, args = (conn, addr))
  thread.start()
  send(conn,"hello world from server")
  print("new conn", threading.activeCount()-1)




