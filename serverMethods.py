import string
import random
import os


# this method creates a new random identifier for the client
def createIdentifier():
    length = 128
    random_identifier = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=length))
    return str(random_identifier)


# this method creates a new file for the specified identifier on the server
def createNewClient(identifier):
    path = getPath(identifier)
    os.mkdir(path)


# this method returns the current path we need to update
def getPathToWrite(path, path_to_join):
    path = os.path.join(path, path_to_join)
    return path


# this method returns the path directory of the given identifier
def getPath(identifier):
    parent_dir = os.getcwd()
    directory_name = identifier
    path = os.path.join(parent_dir, directory_name)
    return path

def createNewFolder(path, folder_name):
    path = os.path.join(path, folder_name)
    print("the file" + folder_name + "has been created")
    os.mkdir(path)

def createNewFile(path, file_name):
    path = os.path.join(path, file_name)
    open(path, 'w')
