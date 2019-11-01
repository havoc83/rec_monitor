import sys
import time
import logging

import redis
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src import events

def main():
    r_conn = redis.Redis(host='redis')

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = FileSystemEventHandler()
    event_handler.on_any_event = lambda event: print(f"hey, {event.src_path} has been created!")
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
