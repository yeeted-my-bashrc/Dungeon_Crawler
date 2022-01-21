#!/usr/bin/python3
# THIS ALLOWS YOU TO RUN AS ./filename.py
# give permission by: chmod +x filename.py

import socket
import time
import threading
from utils import *
import pygame
import sys
import pickle

# sets terminal window caption. not sure if this only works on linux
sys.stdout.write("\x1b]2;Client\x07")

# socket for client
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_IP = input("server_IP:")
s.connect((server_IP, 50000))

headerSize = 10
running = True

screenWidth = 800
screenHeight = 800

pygame.display.init()
pygame.mixer.init()

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Dungeon Crawler")


def send(msg):
    # this encodes msg and sets a header which represents msg length, I think
    msg = f"{msg}".encode()
    msg = bytes(f"{len(msg):<{headerSize}}", "utf-8") + msg
    s.send(msg)


headerSize = 10
msglen = 100  # just to set it to something
dungeon = Dungeon()
player = Player(Rect(0, 0, 48, 48), pygame.image.load("/images/default_char.png"))


def receive(conn, addr):
    global headerSize, msglen, dungeon, player
    while running:
        msg_buffer = b""
        new_msg = True
        while True:

            # Now i know exactly how this works. I would like to do google meet to explain it.
            if len(msg_buffer) < msglen:
                msg = conn.recv(1024)
                msg_buffer += msg

            if new_msg:
                msglen = int(msg_buffer[:headerSize])
                new_msg = False

            # this is when it knows it received the whole message, and then decodes it
            if len(msg_buffer) - headerSize >= msglen:
                decoded_msg = msg_buffer[headerSize : headerSize + msglen].decode()
                print(headerSize, msglen, "full message: ", decoded_msg)
                if decoded_msg[0] == "1":
                    msgList = decoded_msg.split(":")
                    player.rect.x = msgList[1]
                    player.rect.y = msgList[2]
                    dungeon.map = pickle.loads(msgList[3])
                new_msg = True
                msg_buffer = msg_buffer[headerSize + msglen :]


recv_thread = threading.Thread(target=receive, args=(s, server_IP))
recv_thread.start()

while running:
    time.sleep(1e6)
