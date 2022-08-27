import socket
import sys
import time

import utils
from watchdog.observers import Observer

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
pc_num = 0


# the function is used to send the pc number to the server.
def send_pc_num(sock):
    global pc_num
    sock.send(str(pc_num).encode('utf-8'))
    if pc_num != 0:
        return
    pc_num = int(sock.recv(100).decode())
    sock.send(b'hi')


# restarts the observer in order to start the observer again.
def restart_observer(handler):
    global path
    observer = Observer()
    observer.schedule(handler, path, recursive=True)
    observer.start()
    return observer


def sync(sock):
    global path, timeOut
    # creates a watchdog handler to handle all the changes and starts observer
    handler = utils.Handler(path)
    observer = restart_observer(handler)
    linux_modified = False
    try:
        while True:
            # if the sock is not none it means we are already connected to the server, so we don't need to connect again
            if sock is None:
                # If we aren't connected to the server we will sleep for a few seconds.
                time.sleep(timeOut)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, port))
                # If the client already have an identifier he sends it to the server.
                sock.send(identifier.encode('utf-8'))
                sock.recv(100)
                send_pc_num(sock)
                sock.recv(100).decode('utf-8')
            # we go through each change the observer caught and sends its details to the server with utils.send_sync
            for change in handler.changes:
                event_type = change[0]
                is_folder = change[1]
                src_path = change[2]
                dst_path = change[3]
                if change[0] != 'moved':
                    linux_modified = utils.send_sync(sock, path, event_type, is_folder, src_path, dst_path,
                                                     linux_modified)
                else:
                    linux_modified = utils.send_sync(sock, path, event_type, is_folder, src_path, dst_path,
                                                     linux_modified)
            # when we sent all the changes we reset the list of changes and stop the observer in order to get the
            # changes from the server
            handler.reset_changes()
            sock.send(b'I have finished')
            observer.stop()
            utils.update_file(sock, path)
            # after we got all the changes, we start the observer again, close the connection and start again.
            observer = restart_observer(handler)
            sock.close()
            sock = None
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
    # loops over all the changed and sends the right parameters to send_sync


while True:
    # gets the socket from the os and connects to the server
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # if this is a new client it notifies the server that he is new and gets is notifier and then sends everything
    # inside the folder and sub folder to the server
    if identifier is None:
        sckt.connect((ip, port))
        sckt.send("Hello, i am new here".encode('utf-8'))
        sckt.recv(100)
        send_pc_num(sckt)
        identifier = sckt.recv(130).decode('utf-8')
        f = open('identifier.txt', 'w')
        f.write(identifier)
        f.close()
        utils.send_all(path, sckt)
        sckt.close()
        sync(None)
    else:
        sckt.connect((ip, port))
        # If the client already have an identifier he sends it to the server.
        sckt.send(identifier.encode('utf-8'))
        sckt.recv(100)
        send_pc_num(sckt)
        message = sckt.recv(100).decode('utf-8')
        # If the server found the identifier and the client folder is empty, the server sends the client everything
        if message == "found you, new":
            utils.recv_file(sckt, path)
        # if the server found the identifier then it syncs all the new changes with the client.
        elif message == "found you!":
            sync(sckt)
        # If the server didn't find the identifier then the client sends everything to the server
        else:
            utils.send_all(path, sckt)
        sckt.close()
