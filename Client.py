import socket
import sys
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


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
files = os.walk(path, True)
finishMessage = "I have finished"


def recvFile():
    s.send("empty directory".encode('utf-8'))
    message = s.recv(100).decode('utf-8')
    while message != finishMessage:
        currPath = path
        while message != "the directories are:":
            message = s.recv(100).decode('utf-8')
            s.send(b'hi')
            os.path.join(currPath, message)
        while message != "the files are:":
            message = s.recv(100).decode('utf-8')
            s.send(b'hi')
            dirPath = os.path.join(currPath, message)
            os.mkdir(dirPath)
        while message != "the path is:" or message != finishMessage:
            message = s.recv(100).decode('utf-8')
            s.send(b'hi')
            filePath = os.path.join(currPath, message)
            file = open(filePath, "wb")


def sendAll():
    global identifier, files
    files = os.walk(path, True)
    for (dirpath, dirnames, filename) in files:
        s.send("the path is:".encode('utf-8'))
        s.recv(100)
        localPath = str(dirpath).removeprefix(path)
        seperator = ""
        if path.find('\\'):
            seperator = '\\'
        else:
            seperator = '/'
        pathToFolder = localPath.split(seperator)
        if len(pathToFolder) > 1:
            for i in range(1, len(pathToFolder)):
                s.send(pathToFolder[i].encode('utf-8'))
                s.recv(100)
        s.send("the directories are:".encode('utf-8'))
        s.recv(100)
        for directory in dirnames:
            s.send(directory.encode('utf-8'))
            s.recv(100)
        s.send("the files are:".encode('utf-8'))
        s.recv(100)
        for file in filename:
            filepath = os.path.join(dirpath, file)
            filesize = str(os.path.getsize(filepath))
            s.send(file.encode('utf-8'))
            s.recv(100)
            s.send(filesize.encode('utf-8'))
            s.recv(100)
            f = open(filepath, "rb")
            while True:
                bytes_read = f.read(4096)
                if not bytes_read:
                    break
                s.send(bytes_read)
            s.recv(100)
            f.close()


def sync():
    return None


# while True:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))
if identifier is None:
    s.send("Hello, i am new here".encode('utf-8'))
    identifier = s.recv(130).decode('utf-8')
    print(identifier)
    sendAll()
else:
    s.send(identifier.encode('utf-8'))
    message = s.recv(100).decode('utf-8')
    if message == "found you!":
        sync()
    elif message == "found you!" and len(os.listdir(path)) == 0:
        recvFile()
    else:
        sendAll()
s.send(finishMessage.encode('utf-8'))
s.close()
