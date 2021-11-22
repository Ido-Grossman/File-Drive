import os
import string
import random
from watchdog.events import FileSystemEventHandler


class Handler(FileSystemEventHandler):
    def __init__(self, path):
        self.changes = list()
        self.path = path

    def on_any_event(self, event):
        if event.event_type == 'closed' or (event.event_type == 'modified' and event.src_path == self.path):
            return
        if event.event_type == 'moved':
            details = (event.event_type, event.is_directory, event.src_path, event.dest_path)
        else:
            details = (event.event_type, event.is_directory, event.src_path)
        self.changes.append(details)

    def reset_changes(self):
        self.changes.clear()


def remove_prefix(to_remove, string1):
    if string1.startswith(to_remove):
        string1 = string1.lstrip(to_remove)
    return string1


def send_file(socket, file_path):
    # gets the size of the file and sends it to the other side
    filesize = str(os.path.getsize(file_path))
    socket.send(filesize.encode('utf-8'))
    socket.recv(100)
    # we open the file in read bytes mode and send all the bytes in the file to the other side.
    f = open(file_path, "rb")
    while True:
        bytes_read = f.read(4096)
        if not bytes_read:
            break
        socket.send(bytes_read)
    f.close()


# Used to send files to the other side, it gets the socket, path to the folder it syncs = path_to_main,
# path to the current folder he is in = path_to_folder, directories and files inside the folder
def send_files(socket, path_to_main, path_to_folder, directories, files):
    # it sets the local path of the folder we are in now and notifies the server that he sends the path
    try:
        local_path = str(path_to_folder).removeprefix(path_to_main)
    except:
        local_path = remove_prefix(path_to_main, path_to_folder)
    socket.send("the path is:".encode('utf-8'))
    socket.recv(100)
    separator = os.sep
    folders = local_path.split(separator)
    if len(folders) > 1:
        for i in range(1, len(folders)):
            socket.send(folders[i].encode('utf-8'))
            socket.recv(100)
    socket.send("the directories are:".encode('utf-8'))
    socket.recv(100)
    # after it finished sending the path it sends all the directories in the path
    for directory in directories:
        socket.send(directory.encode('utf-8'))
        socket.recv(100)
    # after it finished sending all the directories in the path if sends all the files in the path
    socket.send("the files are:".encode('utf-8'))
    socket.recv(100)
    for file in files:
        # it gets the path to the file and gets is size and name and sends them to the server
        filepath = os.path.join(path_to_folder, file)
        socket.send(file.encode('utf-8'))
        socket.recv(100)
        send_file(socket, filepath)
        socket.recv(100)


def recv_file(socket, path_to_main):
    message = socket.recv(100).decode('utf-8')
    # while the other side didn't finish sending all the files it tries to get to the next path
    while message != "I have finished":
        # saves the path we currently in
        curr_path = path_to_main
        socket.send(b'hi')
        message = socket.recv(100).decode('utf-8')
        while message != "the directories are:":
            curr_path = os.path.join(curr_path, message)
            socket.send(b'hi')
            message = socket.recv(100).decode('utf-8')
        socket.send(b'hi')
        message = socket.recv(100).decode('utf-8')
        while message != "the files are:":
            # until we get the message "the files are:" it means we still get the directories so we create them.
            socket.send(b'hi')
            dir_path = os.path.join(curr_path, message)
            os.mkdir(dir_path)
            message = socket.recv(100).decode('utf-8')
        socket.send(b'hi')
        message = socket.recv(100).decode('utf-8')
        while message != "the path is:":
            # until the other side has finished or sends us another path we create the files in the path
            # we get the name and size of file each time and open the file
            if message == "I have finished":
                break
            socket.send(b'hi')
            file_path = os.path.join(curr_path, message)
            message = socket.recv(100).decode('utf-8')
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
            socket.send(b'finished')
            file.close()
            message = socket.recv(100).decode('utf-8')


def create_identifier():
    length = 128
    random_identifier = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=length))
    return str(random_identifier)


# this method creates a new file for the specified identifier on the server
def create_new_client(identifier):
    path = get_path(identifier)
    os.mkdir(path)
    return path


# this method returns the path directory of the given identifier
def get_path(identifier):
    parent_dir = os.getcwd()
    directory_name = identifier
    path = os.path.join(parent_dir, directory_name)
    return path


def no_identifier(identifier):
    return None


def update_file(identifier):
    return None


# sends all the files that are in the folder
def send_all(path, socket):
    # gets all the files in the folder and for folder inside it sends all the files and folders it contains
    files = os.walk(path, True)
    for (dirpath, dirnames, filenames) in files:
        send_files(socket, path, dirpath, dirnames, filenames)
    # when it finished sending all the files it notifies the server
    socket.send("I have finished".encode('utf-8'))


def send_path(socket, separator, path_to_main, path_to_folder):
    # sends this os folders separator to the other side.
    socket.send(separator.encode('utf-8'))
    socket.recv(2)
    socket.send(os.path.relpath(path_to_folder, path_to_main).encode('utf-8'))
    socket.recv(2)
    return
    # sends this os folders separator to the other side.
    socket.send(separator.encode('utf-8'))
    socket.recv(2)
    # sends the absolute path to the main directory on this pc.
    socket.send(path_to_main.encode('utf-8'))
    socket.recv(2)
    # sends the absolute path to the folder on this pc.
    socket.send(path_to_folder.encode('utf-8'))
    socket.recv(2)


def send_sync(socket, path_to_main, event_type, is_directory, src_path, dest_path):
    # sends the event type of the file/folder (whether it moved/modified/ext.)
    socket.send(event_type.encode('utf-8'))
    socket.recv(2)
    # send true if it's a directory and false otherwise.
    socket.send(str(is_directory).encode('utf-8'))
    socket.recv(2)
    # gets the os folders separator.
    separator = os.sep
    # send the separator
    send_path(socket, separator, os.path.abspath(path_to_main), os.path.abspath(src_path))
    if dest_path is not None:
        send_path(socket, separator, os.path.abspath(path_to_main), os.path.abspath(dest_path))
    elif event_type == 'modified' and not is_directory:
        send_file(socket, src_path)
    socket.recv(100)
