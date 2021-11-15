from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class Handler(FileSystemEventHandler):
    def on_any_event(self, event):
        return None

    def on_deleted(self, event):
        return None

    def on_closed(self, event):
        return None

    def on_moved(self, event):
        return None

    def on_created(self, event):
        return None

    def on_modified(self, event):
        return None
