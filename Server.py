import os
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
        num_of_users_per_identifier[identifier] = {1: []}
        client_socket.send(identifier.encode())  # sending the identifier
        path = utils.create_new_client(identifier)  # then we create the file with the name of the identifier
        utils.recv_file(client_socket, path)

    else:
        number_of_users = num_of_users_per_identifier.get(identifier)
        if number_of_users is None:
            client_socket.send(b'1')  # sending the number of pc
            client_socket.recv(100)
            client_socket.send(b'not found')
            num_of_users_per_identifier[identifier] = {1: []}
            print(identifier)
            path = utils.create_new_client(identifier)
            utils.recv_file(client_socket, path)
        else:       # if the identifier was found

            if int(pc_num) == 0:
                number_of_users = sorted(num_of_users_per_identifier[identifier].keys())[-1]
                number_of_users += 1
                num_of_users_per_identifier[identifier][number_of_users] = []
                client_socket.send(str(number_of_users).encode())
                client_socket.recv(100)
                client_socket.send(b'found you, new')
                utils.send_all(identifier, client_socket)

            else:
                is_updated = False
                client_socket.send(b'found you!')
                changed_things = utils.update_file(client_socket, identifier, int(pc_num))
                curr_dict = num_of_users_per_identifier[identifier]
                for keys in curr_dict:
                    if int(pc_num) == keys or not changed_things:
                        continue
                    curr_dict[keys].append(changed_things)
                for changes in curr_dict[int(pc_num)]:
                    for change in changes:
                        is_updated = True
                        src_path = os.path.join(identifier, change[2])
                        if change[0] != 'moved':
                            utils.send_sync(client_socket, identifier, change[0], change[1], src_path, None)
                        else:
                            dst_path = os.path.join(identifier, change[3])
                            utils.send_sync(client_socket, identifier, change[0], change[1], src_path, dst_path)

                client_socket.send(b'I have finished')
                if is_updated is True:
                    curr_dict[int(pc_num)].clear()
    client_socket.close()
    print('Client disconnected')
