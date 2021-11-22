import os.path

import utils
import time
from watchdog.observers import Observer

path = 'ToSync'
handler = utils.Handler(path)
observer = Observer()
observer.schedule(handler, path, recursive=True)
observer.start()
try:
    while True:
        time.sleep(10)
        for change in handler.changes:
            print(change)
        handler.reset_changes()
except KeyboardInterrupt:
    observer.stop()
    observer.join()
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(('25.84.19.151', 12345))
# s.send(str(True).encode('utf-8'))
# s.close()
