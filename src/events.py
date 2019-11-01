
class events(object):
    def __init__(self, conn, list_name, del_name):
        self.conn = conn
        self.lst = list_name
        self.del_lst = del_name

    def on_create(self, event):
        self.conn.lpush(self.lst, event.src_path)

    def on_modified(self, event):
        self.conn.lpush(self.lst, event.src_path)

    def on_moved(self, event):
        self.conn.mset({event.src_path, event.dest_path})

    def on_delete(self, event):
        self.conn.lpush(self.del_lst, event.src_path)