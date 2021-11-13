import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

class Watcher:
    def __init__(self, directory=".", handler = FileSystemEventHandler()):
        self.observer = Observer()
        self.handler = handler
        self.directory = directory
    def run(self):
        self.observer.schedule(
            self.handler, self.directory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
        self.observer.join()
