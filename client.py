#!/usr/bin/python3
#THIS ALLOWS YOU TO RUN AS ./filename.py
#give permission by: chmod +x filename.py
import socket
import time
import threading
#socket for client
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_IP = input("server_IP:")
s.connect((server_IP,50000))

headerSize=10
running=True

def send(msg):
  #this encodes msg and sets a header which represents msg length, I think
  msg = msg.encode()
  msg = bytes(f"{len(msg):<{headerSize}}",'utf-8')+msg
  s.send(msg)
  print("client send")

def receive():
  while running:
    msg_buffer = b''
    new_msg = True
    while True:


      #so this code basically is the msg buffer. Itruns it. idk i swear i knew what it meant two years ago. for now i guess we can just use it?. I swear i coded this on my own with some help.
      if (new_msg and len(msg_buffer) < headerSize) \
        or (not new_msg and len(msg_buffer) < headerSize+msglen):
        msg = s.recv(1024)
        msg_buffer += msg

      if new_msg:
        msglen = int(msg_buffer[:headerSize])
        new_msg = False

      #this is when it knows it received the whole message, and then decodes it
      if len(msg_buffer)-headerSize >= msglen: # full message
        decoded_msg = msg_buffer[headerSize:headerSize + msglen].decode()

        if decoded_msg=="hello world from server":
          print("hello word from server")

        print(decoded_msg)
      new_msg = True
      msg_buffer = msg_buffer[headerSize+msglen:]

recv_thread = threading.Thread(target=receive)
recv_thread.start()
while running:
  send("hello word from client")
  time.sleep(1);