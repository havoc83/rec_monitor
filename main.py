import sys
import time
import logging
import configparser
import redis

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src import events

def create_db_conn(db_config):

    return redis.Redis(host=db_config.get('host', 'redis'),
                       port=db_config.getint('port', 6379),
                       db=db_config.getint('db', 0))

def get_config(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    return config

def create_handler(handlers):
    event_handler = FileSystemEventHandler()
    event_handler.on_any_event = lambda event: print(f"hey, {event.src_path} has been created!")
    return event_handler

def create_observer(handler, path, recurse):
    observer = Observer()
    observer.schedule(handler, path, recursive=recurse)
    return observer


def main():
    """
    """
    config = get_config("monitor.ini")
    conn = create_db_conn(config['database'])
    
    if 'debug' in sys.argv:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
        
    logging.basicConfig(level=log_level,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')


    path = config['monitor'].get('path','.')
    recurse = config['monitor'].getboolean('recursive')
    table = config['database'].get('hash_name', 'files')
    handlers = create_handler(events.Events(conn, table))

    observer = get_observer(handlers, path, recurse)
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
