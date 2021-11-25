import socket
import time
from watchdog.observers import Observer
import utils

handler = utils.Handler('ToSync')
observer = Observer()
observer.schedule(handler, 'ToSync', recursive=True)
observer.start()
try:
    while True:
        time.sleep(15)
        print(handler.changes)
        handler.reset_changes()
except KeyboardInterrupt:
    observer.stop()
observer.join()

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(('25.84.19.151', 12345))
# s.send(str(True).encode('utf-8'))
# s.close()
