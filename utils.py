import os


def sendFiles(socket, path_to_main, path_to_folder, directories, files):
    local_path = str(path_to_folder).removeprefix(path_to_main)
    socket.send("the path is:".encode('utf-8'))
    socket.recv(100)
    if path_to_main.find('\\'):
        separator = '\\'
    else:
        separator = '/'
    path_to_folder = local_path.split(separator)
    if len(path_to_folder) > 1:
        for i in range(1, len(path_to_folder)):
            socket.send(path_to_folder[i].encode('utf-8'))
            socket.recv(100)
    socket.send("the directories are:".encode('utf-8'))
    socket.recv(100)
    for directory in directories:
        socket.send(directory.encode('utf-8'))
        socket.recv(100)
    socket.send("the files are:".encode('utf-8'))
    socket.recv(100)
    for file in files:
        filepath = os.path.join(str(path_to_folder), file)
        filesize = str(os.path.getsize(filepath))
        socket.send(file.encode('utf-8'))
        socket.recv(100)
        socket.send(filesize.encode('utf-8'))
        socket.recv(100)
        f = open(filepath, "rb")
        while True:
            bytes_read = f.read(4096)
            if not bytes_read:
                break
            socket.send(bytes_read)
        socket.recv(100)
        f.close()


def recvFile(socket, path_to_main):
    socket.send("empty directory".encode('utf-8'))
    message = socket.recv(100).decode('utf-8')
    while message != "I have finished":
        curr_path = str(path_to_main)
        while message != "the directories are:":
            message = socket.recv(100).decode('utf-8')
            socket.send(b'hi')
            os.path.join(curr_path, message)
        while message != "the files are:":
            message = socket.recv(100).decode('utf-8')
            socket.send(b'hi')
            dir_path = os.path.join(curr_path, message)
            os.mkdir(dir_path)
        while message != "the path is:" or message != "I have finished":
            message = socket.recv(100).decode('utf-8')
            socket.send(b'hi')
            file_path = os.path.join(curr_path, message)
            message = socket.recv(100).decode()
            socket.send(b'hi')
            file_size = int(message)
            file = open(file_path, "wb")
            counter = 0
            while counter < file_size:
                # read 1024 bytes from the socket (receive)
                bytes_read = socket.recv(100000)
                counter += len(bytes_read)
                # write to the file the bytes we just received
                file.write(bytes_read)
            file.close()
