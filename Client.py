import socket
import sys

if len(sys.argv) != 4:
    exit(-1)
ip = sys.argv[1]
port = int(sys.argv[2])
path = sys.argv[3]
timeOut = int(sys.argv[4])
if len(sys.argv) == 5:
    identifier = sys.argv[5]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))
s.send(b'Ido Grossman: 208985424')
data = s.recv(100)
print("Server sent: ", data)
s.close()
