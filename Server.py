import socket
import sys
import utils

SEPARATOR = "<SEPARATOR>"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
num_of_users_per_identifier = {}
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
    client_socket.send(b'pc num?')
    pc_num = client_socket.recv(100).decode('utf8')
    # if there is no identifier we get the hello... message
    if identifier == "Hello, i am new here":
        # we create a random identifier and sending it to the client
        client_socket.send(b'1')    # sending the number of pc
        identifier = utils.create_identifier()
        client_socket.recv(100)
        print(identifier)
        num_of_users_per_identifier[identifier] = 1
        client_socket.send(identifier.encode())  # sending the identifier
        path = utils.create_new_client(identifier)  # then we create the file with the name of the identifier
        utils.recv_file(client_socket, path)

    else:
        number_of_users = num_of_users_per_identifier.get(identifier)
        if number_of_users is None:
            client_socket.send(b'1')  # sending the number of pc
            client_socket.recv(100)
            client_socket.send(b'not found')
            num_of_users_per_identifier[identifier] = 1
            print(identifier)
            path = utils.create_new_client(identifier)
            utils.recv_file(client_socket, path)
        else:       # if the identifier was found

            if int(pc_num) == 0:
                number_of_users += 1
                num_of_users_per_identifier[identifier] = number_of_users
                client_socket.send(str(number_of_users).encode())
                client_socket.recv(100)
                client_socket.send(b'found you, new')
                utils.send_all(identifier, client_socket)

            else:
                client_socket.send(b'found you!')
                utils.update_file(client_socket, identifier, int(pc_num))

    client_socket.close()
    print('Client disconnected')
