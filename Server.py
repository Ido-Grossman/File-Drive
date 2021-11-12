import socket
import sys
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
portNum = sys.argv[1]
server.bind(('', portNum))
server.listen(5)
while True:

    print("waiting for connection")
    client_socket, client_address = server.accept()
    print('Connection from: ', client_address)
    data = client_socket.recv(100)
    print('Received: ', data)
    client_socket.send(data.upper())
    print("Sent:", data.upper())
    data = client_socket.recv(100)
    print('Received: ', data)
    client_socket.send(data.upper())
    print("Sent:", data.upper())
    client_socket.close()
    print('Client disconnected')