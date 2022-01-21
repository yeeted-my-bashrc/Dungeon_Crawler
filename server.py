#!/usr/bin/python3
# THIS ALLOWS YOU TO RUN AS ./filename.py
# give permission by: chmod +x filename.py
import socket
import threading
import pygame
import sys
import pickle
import urllib
import time
from utils import *

try:
    import pyperclip as pc
except ModuleNotFoundError:
    print(
        'Massimo: copy/paste "pip install pyperclip" into terminal to automatically copy server IP for convenience. ctrl+shift+v to paste into terminal'
    )

def get_internal_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return str(IP)
# sets terminal window caption. not sure if this only works on linux
sys.stdout.write("\x1b]2;Server\x07")
running = True


# create server socket
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# binds socket to a host and port
s.bind(("0.0.0.0", 50000))
print("bound to all addresses on port 50000")
pc.copy(get_internal_ip())

# socket listens for up to 5 connections
s.listen(5)

connections = []


def send(conn, msg):
    # this encodes msg and sets a header which represents msg length, I think
    msg = f"{msg}".encode()
    msg = bytes(f"{len(msg):<{headerSize}}", "utf-8") + msg
    conn.send(msg)


spawnX = 0
spawnY = 0
dungeon = Dungeon()


def main():
    global spawnX, spawnY, dungeon
    spawnCoords = dungeon.generateMap()
    spawnX = spawnCoords[0]
    spawnY = spawnCoords[1]


headerSize = 10
msglen = 100
receiveThreads = []


def receive(conn, addr):
    global headerSize, msglen
    while running:
        msg_buffer = b""
        new_msg = True
        while True:

            # Now i know exactly how this works. I would like to do google meet to explain it.
            if len(msg_buffer) < msglen:
                msg = conn.recv(1024)
                msg_buffer += msg
                print(msg_buffer)

            if new_msg:
                msglen = int(msg_buffer[:headerSize])
                new_msg = False

            # this is when it knows it received the whole message, and then decodes it
            if len(msg_buffer) - headerSize >= msglen:
                decoded_msg = msg_buffer[headerSize : headerSize + msglen].decode()
                print(headerSize, msglen, "full message: ", decoded_msg)

                new_msg = True
                msg_buffer = msg_buffer[headerSize + msglen :]

    time.sleep(0.08)


mainThread = threading.Thread(target=main)
mainThread.start()
while running:
    conn, addr = s.accept()
    connections.append(conn)
    receiveThreads.append(threading.Thread(target=receive, args=(conn, addr)))
    receiveThreads[-1].start()
    send(connections[-1], f"1:{spawnX}:{spawnY}:{pickle.dumps(dungeon.map).decode('latin-1')}")
    send(conn, "hello world from server")
    print("new conn", threading.active_count() - 1)
