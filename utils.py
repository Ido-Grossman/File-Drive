import os
import string
import random


# Used to send files to the other side, it gets the socket, path to the folder it syncs = path_to_main,
# path to the current folder he is in = path_to_folder, directories and files inside the folder
def sendFiles(socket, path_to_main, path_to_folder, directories, files):
    local_path = path_to_folder.removeprefix(path_to_main)
    socket.send("the path is:".encode('utf-8'))
    socket.recv(100)
    path_of_dirs = local_path.split(os.sep)
    if len(path_of_dirs) > 1:
        for i in range(1, len(path_of_dirs)):
            socket.send(path_of_dirs[i].encode('utf-8'))
            socket.recv(100)
    socket.send("the directories are:".encode('utf-8'))
    socket.recv(100)
    for directory in directories:
        socket.send(directory.encode('utf-8'))
        socket.recv(100)
    socket.send("the files are:".encode('utf-8'))
    socket.recv(100)
    for file in files:
        socket.send(file.encode('utf-8'))
        socket.recv(100)
        path_to_file = os.path.join(path_to_folder, file)
        file_size = str(os.path.getsize(path_to_file))
        socket.send(file_size.encode('utf-8'))
        socket.recv(100)
        f = open(path_to_file, "rb")
        while True:
            bytes_read = f.read(4096)
            if not bytes_read:
                break
            socket.send(bytes_read)
        socket.recv(100)
        f.close()

def createIdentifier():
    length = 128
    random_identifier = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=length))
    return str(random_identifier)


# this method creates a new file for the specified identifier on the server
def createNewClient(identifier):
    path = getPath(identifier)
    os.mkdir(path)
    return path

# this method returns the path directory of the given identifier
def getPath(identifier):
    parent_dir = os.getcwd()
    directory_name = identifier
    path = os.path.join(parent_dir, directory_name)
    return path
