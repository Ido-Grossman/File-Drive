import socket
import sys
import os
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
pcNum = 0
handler = utils.Handler()
watcher = utils.Watcher(path, handler)


def send_pc_num(socket):
    global pcNum
    socket.recv(100)
    socket.send(str(pcNum).encode('utf-8'))
    if pcNum != 0:
        return
    pcNum = int(socket.recv(100).decode())
    socket.send(b'hi')


def sync(socket, changes):
    # loops over all the changed and sends the right parameters to send_sync
    for change in changes:
        if change[0] != 'moved':
            utils.send_sync(socket, path, change[0], change[1], change[2], None)
        else:
            utils.send_sync(socket, path, change[0], change[1], change[2], change[3])
    socket.send(b'I have finished')


while True:
    # gets the socket from the os and connects to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    # if this is a new client it notifies the server that he is new and gets is notifier and then sends everything
    # inside the folder and subfolder to the server
    if identifier is None:
        s.send("Hello, i am new here".encode('utf-8'))
        send_pc_num(s)
        identifier = s.recv(130).decode('utf-8')
        f = open('identifier.txt', 'w')
        f.write(identifier)
        utils.send_all(path, s)
    else:
        # If the client already have an identifier he sends it to the server.
        s.send(identifier.encode('utf-8'))
        send_pc_num(s)
        message = s.recv(100).decode('utf-8')
        # if the server found the identifier then it syncs all the new changes with the client.
        if message == "found you, new":
            utils.recv_file(s, path)
        # If the server found the identifier and the client folder is empty, the server sends the client everything
        elif message == "found you!":
            sync(s, handler.changes)
        # If the server didn't find the identifier then the client sends everything to the server
        else:
            utils.send_all(path, s)
    s.close()
    print("finished sending")
    handler.reset_changes()
    watcher.run(timeOut)
    print("finished timeout")
