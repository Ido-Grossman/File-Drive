import socket
import sys
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

files = list()
if len(sys.argv) < 5:
    exit(-1)
identifier = None
ip = sys.argv[1]
port = int(sys.argv[2])
path = sys.argv[3]
timeOut = int(sys.argv[4])
if len(sys.argv) == 6:
    identifier = sys.argv[5]
files = os.walk(path, True)


def noIdentifier():
    global identifier, files
    s.send("Hello, i am new here".encode('utf-8'))
    identifier = s.recv(128).decode('utf-8')
    files = os.walk(path, True)
    for (dirpath, dirnames, filename) in files:
        s.send(("the path is:" + dirpath).encode('utf-8'))
        s.send("the directories are:".encode('utf-8'))
        for directory in dirnames:
            s.send(directory.encode('utf-8'))
        s.send("the files are:".encode('utf-8'))
        for file in filename:
            s.send(file.encode('utf-8'))


# while True:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))
if identifier is None:
    noIdentifier()
s.close()
