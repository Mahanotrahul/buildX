import redis

class db:
    def __init__(self, db_type):
        self.db_type = db_type

    def create_connection(self):
        if self.db_type == 'redis':
            r = redis.Redis(host = '127.0.0.1', port = 6379, db=1)
            return r       