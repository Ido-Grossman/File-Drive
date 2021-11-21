import utils
import os
import socket

handler = utils.Handler()
w = utils.Watcher('ToSync', handler)
w.run(15)
print(handler.changes)
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(('25.84.19.151', 12345))
# s.send(str(True).encode('utf-8'))
# s.close()
