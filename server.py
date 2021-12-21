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

msg=''

connections = []

def send(msg):
  for i in connections:
    i.send(msg);

headerSize=10
def receive():
  while running and len(connections)>0:
    msg_buffer = b''
    new_msg = True
    while True:

      #so this code basically is the msg buffer. Itruns it. idk i swear i knew what it meant two years ago. for now i guess we can just use it?. I swear i coded this on my own with some help.
      if (new_msg and len(msg_buffer) < headerSize) \
        or (not new_msg and len(msg_buffer) < headerSize+msglen):
        msg = conn.recv(1024)
        msg_buffer += msg

      if new_msg:
        msglen = int(msg_buffer[:headerSize])
        new_msg = False
      print(msg_buffer)

      #this is when it knows it received the whole message, and then decodes it
      if len(msg_buffer)-headerSize >= msglen: # full message
        decoded_msg = msg_buffer[headerSize:headerSize + msglen].decode()

        if decoded_msg=="hello world from client":
          print("hello word from client")

        print(decoded_msg)
      new_msg = True
      msg_buffer = msg_buffer[headerSize+msglen:]

recv_thread = threading.Thread(target=receive)
recv_thread.start()

while running:
  conn, addr = s.accept()
  connections.append(conn);
  send("hello world from server")
  print("new conn")




