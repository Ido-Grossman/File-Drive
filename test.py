import socket

s = {1 : {3 : [5], 2 : [6]}}
print(sorted(s[1].keys())[-1])
print(s)
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(('25.84.19.151', 12345))
# s.send(str(True).encode('utf-8'))
# s.close()
