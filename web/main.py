import time

import redis
from flask import Flask

from controller import database_connector

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

@app.route('/')
def hello():
    return 'Hello World Its me'

@app.route('/api/databaseconnector')
def database_connect():
    query = 'INSERT INTO ecommerce (id_ecommerce,nama_ecommerce) VALUES ("2", "Tokopedia")'
    db = database_connector.Database()
    return db.run(query)

if __name__ == '__main__':
    app.run()