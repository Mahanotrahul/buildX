import string
import random
from db import db
from hashlib import md5
import json

db = db('redis').create_connection()

class Shortener():
    alphabets = string.ascii_letters + string.digits

    def __init__(self):
        pass

    def get_short_url(self, shortcode, scheme, host) -> str:
        hash = md5((scheme + host + shortcode).encode('utf-8')).hexdigest()
        data = db.get(hash)
        if data:
            return json.loads(data)['url']
        else:
            return "empty"

    def set_short_code(self, data, scheme, host) -> str:
        code = ''.join([random.choice(Shortener.alphabets) for _ in range(8)])
        hash = md5((scheme + host + code).encode('utf-8')).hexdigest()
        while db.get(hash):
            code = ''.join([random.choice(Shortener.alphabets) for _ in range(8)])
            hash = md5((scheme + host + code).encode('utf-8')).hexdigest()
        data['code'] = code
        db.set(hash, str(json.dumps(data)), ex=100)
        return code