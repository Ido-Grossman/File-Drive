import os


# Used to send files to the other side, it gets the socket, path to the folder it syncs = path_to_main,
# path to the current folder he is in = path_to_folder, directories and files inside the folder
def sendFiles(socket, path_to_main, path_to_folder, directories, files):
    # it sets the local path of the folder we are in now and notifies the server that he sends the path
    local_path = str(path_to_folder).removeprefix(path_to_main)
    socket.send("the path is:".encode('utf-8'))
    socket.recv(100)
    # it finds how the folder are seperated in the os and splits them and sends each folder by order to get into the
    # desired path
    separator = os.sep
    path_to_folder = local_path.split(separator)
    if len(path_to_folder) > 1:
        for i in range(1, len(path_to_folder)):
            socket.send(path_to_folder[i].encode('utf-8'))
            socket.recv(100)
    # after it finished sending the path it sends all the directories in the path
    socket.send("the directories are:".encode('utf-8'))
    socket.recv(100)
    for directory in directories:
        socket.send(directory.encode('utf-8'))
        socket.recv(100)
    # after it finished sending all the directories in the path if sends all the files in the path
    socket.send("the files are:".encode('utf-8'))
    socket.recv(100)
    for file in files:
        # it gets the path to the file and gets is size and name and sends them to the server
        filepath = os.path.join(str(path_to_folder), file)
        filesize = str(os.path.getsize(filepath))
        socket.send(file.encode('utf-8'))
        socket.recv(100)
        socket.send(filesize.encode('utf-8'))
        socket.recv(100)
        # we open the file in read bytes mode and send all the bytes in the file to the server.
        f = open(filepath, "rb")
        while True:
            bytes_read = f.read(4096)
            if not bytes_read:
                break
            socket.send(bytes_read)
        socket.recv(100)
        f.close()


def recvFile(socket, path_to_main):
    message = socket.recv(100).decode('utf-8')
    # while the other side didn't finish sending all the files it tries to get to the next path
    while message != "I have finished":
        # saves the path we currently in
        curr_path = str(path_to_main)
        while message != "the directories are:":
            # until we get the message "the directories are:" it means the other side still sends us the path
            # so we join each folder to the current path
            message = socket.recv(100).decode('utf-8')
            socket.send(b'hi')
            os.path.join(curr_path, message)
        while message != "the files are:":
            # until we get the message "the files are:" it means we still get the directories so we create them.
            message = socket.recv(100).decode('utf-8')
            socket.send(b'hi')
            dir_path = os.path.join(curr_path, message)
            os.mkdir(dir_path)
        while message != "the path is:" or message != "I have finished":
            # until the other side has finished or sends us another path we create the files in the path
            # we get the name and size of file each time and open the file
            message = socket.recv(100).decode('utf-8')
            socket.send(b'hi')
            file_path = os.path.join(curr_path, message)
            message = socket.recv(100).decode()
            socket.send(b'hi')
            file_size = int(message)
            file = open(file_path, "wb")
            counter = 0
            # until we finished reading all the file, we will receive the next bytes and write them to the file.
            while counter < file_size:
                # read 1024 bytes from the socket (receive)
                bytes_read = socket.recv(100000)
                counter += len(bytes_read)
                # write to the file the bytes we just received
                file.write(bytes_read)
            file.close()