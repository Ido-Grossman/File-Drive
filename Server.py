import socket
import sys
import serverMethods
SEPARATOR = "<SEPARATOR>"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 2:  # if we receive an invalid arguments we exit
    exit(-1)
portNum = int(sys.argv[1])
server.bind(('', portNum))
server.listen(5)
while True:
    print("waiting for connection")
    client_socket, client_address = server.accept()
    print('Connection from: ', client_address)
    data = client_socket.recv(130)  # we receive an identifier from the client at first
    identifier = data.decode('utf8')
    # if there is no identifier we get the hello... message
    if identifier == "Hello, i am new here":
        # we create a random identifier and sending it to the client
        identifier = serverMethods.createIdentifier()
        client_socket.send(identifier.encode())
        serverMethods.createNewClient(identifier)  # then we create the file with the name of the identifier
        data_from_user = client_socket.recv(200)  # then we receive the number of the files and directories to make
        client_socket.send(data_from_user)
        while True:  # if we dont receive anymore data then we are finished
            decodedData = str(data_from_user.decode('utf8'))
            print("ido sent me " + decodedData)
            if decodedData.startswith('the path is:'):
                path = serverMethods.getPath(identifier)
                data_from_user = client_socket.recv(200)
                client_socket.send(data_from_user)
                decodedData = str(data_from_user.decode('utf8'))

                while not decodedData.startswith('the directories are:'):
                    print("ido sent me " + decodedData)
                    path = serverMethods.getPathToWrite(path, decodedData)
                    data_from_user = client_socket.recv(200)
                    client_socket.send(data_from_user)
                    decodedData = str(data_from_user.decode('utf8'))
                    print("the name of the dir is " + decodedData)

            elif decodedData.startswith('the directories are:'):
                data_from_user = client_socket.recv(200)
                client_socket.send(data_from_user)
                decodedData = str(data_from_user.decode('utf8'))
                while not decodedData.startswith('the files are:'):
                    print("the name of the file is " + decodedData)
                    serverMethods.createNewFolder(path, decodedData)
                    data_from_user = client_socket.recv(200)
                    client_socket.send(data_from_user)
                    decodedData = str(data_from_user.decode('utf8'))

            else:
                if decodedData.startswith('the files are:'):
                    data_from_user = client_socket.recv(4096)
                    decodedData = str(data_from_user.decode('utf8'))
                    if decodedData.startswith("the path is:"):
                        client_socket.send(b'gay')
                        continue
                    if decodedData.startswith("I have finished"):
                        break
                    client_socket.send(data_from_user)
                    file_size = client_socket.recv(200)
                    client_socket.send(data_from_user)
                    file_size = int(file_size.decode())
                    counter = 0
                    path = serverMethods.getPathToWrite(path, decodedData)
                    with open(path, "wb") as f:
                        while counter < file_size:
                            # read 1024 bytes from the socket (receive)
                            bytes_read = client_socket.recv(100000)
                            counter += len(bytes_read)
                            # write to the file the bytes we just received
                            f.write(bytes_read)
                        f.close()
                    client_socket.send(b'finished')
                if decodedData.startswith("I have finished"):
                    break
                data_from_user = client_socket.recv(200)
                client_socket.send(data_from_user)
    # if there is an identifier we search the file on the server
    # else:
    #     if searchFile(identifier) is True:
    #         updateFile(identifier)
    #     else:
    #         noIdentifier(identifier)
    client_socket.close()
    print('Client disconnected')