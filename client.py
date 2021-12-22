#!/usr/bin/python3
#THIS ALLOWS YOU TO RUN AS ./filename.py
#give permission by: chmod +x filename.py

#test 2
import socket
import time
import threading
import classes
import pygame

#socket for client
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_IP = input("server_IP:")
s.connect((server_IP,50000))

headerSize=10
running=True

def send(msg):
  #this encodes msg and sets a header which represents msg length, I think
  msg = f'hello world from client'.encode()
  msg = bytes(f"{len(msg):<{headerSize}}",'utf-8')+msg
  s.send(msg)

headerSize=10
msglen=100 #just to set it to something
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

      if new_msg:
        msglen = int(msg_buffer[:headerSize])
        new_msg = False

      #this is when it knows it received the whole message, and then decodes it
      if len(msg_buffer)-headerSize >= msglen:
        decoded_msg = msg_buffer[headerSize:headerSize + msglen].decode()
        print(headerSize,msglen,"full message: ",decoded_msg)

        new_msg = True
        msg_buffer = msg_buffer[headerSize+msglen:]


recv_thread = threading.Thread(target=receive, args = (s,server_IP))
recv_thread.start()

while running:
  send("hello word from client")
  time.sleep(1);