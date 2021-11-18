import socket
import sys
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import utils

# gets the arguments from the user and check if the user sent all the needed arguments as he should
if len(sys.argv) < 5:
    exit(-1)
identifier = None
ip = sys.argv[1]
port = int(sys.argv[2])
path = sys.argv[3]
timeOut = int(sys.argv[4])
if len(sys.argv) == 6:
    if len(sys.argv[5]) != 128:
        exit(-1)
    identifier = sys.argv[5]
trial = os.sep


# sends all the files that are in the folder
def sendAll(socket):
    # gets all the files in the folder and for folder inside it sends all the files and folders it contains
    files = os.walk(path, True)
    for (dirpath, dirnames, filenames) in files:
        utils.sendFiles(socket, path, dirpath, dirnames, filenames)
    # when it finished sending all the files it notifies the server
    socket.send("I have finished".encode('utf-8'))
        


def sync():
    return None


# while True:
# gets the socket from the os and connects to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))
# if this is a new client it notifies the server that he is new and gets is notifier and then sends everything
# inside the folder and subfolder to the server
if identifier is None:
    s.send("Hello, i am new here".encode('utf-8'))
    identifier = s.recv(130).decode('utf-8')
    sendAll(s)
else:
    # If the client already have an identifier he sends it to the server.
    s.send(identifier.encode('utf-8'))
    message = s.recv(100).decode('utf-8')
    # if the server found the identifier then it syncs all the new changes with the client.
    if message == "found you!":
        sync()
    # If the server found the identifier and the client folder is empty, the server sends the client everything
    elif message == "found you!" and len(os.listdir(path)) == 0:
        s.send("empty directory".encode('utf-8'))
        utils.recvFile(s, path)
    # If the server didn't find the identifier then the client sends everything to the server
    else:
        sendAll(s)
s.close()
