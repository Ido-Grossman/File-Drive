import socket
import sys
import serverMethods

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 2:
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
        while len(data_from_user) != 0:  # if we dont receive anymore data then we are finished
            decodedData = str(data_from_user.decode('utf8'))
            if decodedData.startswith('the path is:'):
                path = serverMethods.getPathToWrite(decodedData, identifier)
                data_from_user = client_socket.recv(200)
            elif decodedData.startswith('the directories are:'):
                data_from_user = client_socket.recv(200)
                decodedData = str(data_from_user.decode('utf8'))
                while not decodedData.startswith('the files are:'):
                    serverMethods.createNewFolder(path, decodedData)
                    data_from_user = client_socket.recv(200)
                    decodedData = str(data_from_user.decode('utf8'))
            else:
                if decodedData.startswith('the files are:'):
                    data_from_user = client_socket.recv(200)
                    decodedData = str(data_from_user.decode('utf8'))
                serverMethods.createNewFile(path, decodedData)
                data_from_user = client_socket.recv(200)
    # if there is an identifier we search the file on the server
    # else:
    #     if searchFile(identifier) is True:
    #         updateFile(identifier)
    #     else:
    #         noIdentifier(identifier)
    print('Received: ', identifier)
    client_socket.send(data.upper())
    print("Sent:", identifier.upper())
    client_socket.close()
    print('Client disconnected')