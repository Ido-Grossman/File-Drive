import socket
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

if len(sys.argv) < 5:
    exit(-1)
identifier = None
ip = sys.argv[1]
port = int(sys.argv[2])
path = sys.argv[3]
timeOut = int(sys.argv[4])
if len(sys.argv) == 6:
    identifier = sys.argv[5]


def noIdentifier():
    global identifier
    s.send("Hello, i am new here".encode('utf-8'))
    identifier = s.recv(128).decode('utf-8')
    return None


while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    if identifier is None:
        noIdentifier()
    s.close()
