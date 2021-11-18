import socket
import sys
import serverMethods
import utils

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
        identifier = utils.createIdentifier()
        client_socket.send(identifier.encode())
        path = utils.createNewClient(identifier)  # then we create the file with the name of the identifier
        utils.recvFile(client_socket, path)
    # if there is an identifier we search the file on the server
    # else:
    #     if searchFile(identifier) is True:
    #         updateFile(identifier)
    #     else:
    #         noIdentifier(identifier)
    client_socket.close()
    print('Client disconnected')