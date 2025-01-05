import time
import importlib
import os
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import sssg.cli # circular dependency resolution

class Handler(LoggingEventHandler):
    def on_modified(self, event):
        if os.path.isdir(event.src_path):
            print("{} was ignored (directory)".format(event.src_path))
            return
        print("{} triggered reload".format(event.src_path))
        time.sleep(0.25) # reduce some nvim race conditions
        sssg.cli.main(["", "rebuild"])

    on_created = on_modified

def liveupdate():
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, './src', recursive=True)
    observer.schedule(event_handler, './templates', recursive=True)
    observer.start()
    print("observer started")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
