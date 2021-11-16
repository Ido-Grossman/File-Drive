import socket
import sys
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import utils

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 100000
files = list()
if len(sys.argv) < 5:
    exit(-1)
identifier = None
ip = sys.argv[1]
port = int(sys.argv[2])
path = sys.argv[3]
timeOut = int(sys.argv[4])
if len(sys.argv) == 6:
    if (len(sys.argv[5]) < 128):
        exit(-1)
    identifier = sys.argv[5]
finishMessage = "I have finished"


def sendAll(socket):
    files = os.walk(path, True)
    for (dirpath, dirnames, filenames) in files:
        utils.sendFiles(socket, path, dirpath, dirnames, filenames)
        


def sync():
    return None


# while True:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))
if identifier is None:
    s.send("Hello, i am new here".encode('utf-8'))
    identifier = s.recv(130).decode('utf-8')
    print(identifier)
    sendAll(s)
else:
    s.send(identifier.encode('utf-8'))
    message = s.recv(100).decode('utf-8')
    if message == "found you!":
        sync()
    elif message == "found you!" and len(os.listdir(path)) == 0:
        utils.recvFile(s, path)
    else:
        sendAll(s)
s.send(finishMessage.encode('utf-8'))
s.close()
