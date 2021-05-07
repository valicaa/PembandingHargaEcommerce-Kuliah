import time

import redis
from flask import Flask, render_template, send_file

from controller import database_connector
from scraper import shopee

app = Flask(__name__, static_url_path='/static')
cache = redis.Redis(host='redis', port=6379)

@app.route('/')
def hello():
    return 'Hello World Its me'

@app.route('/api/databaseconnector')
def database_connect():
    query = 'INSERT INTO ecommerce (id_ecommerce,nama_ecommerce) VALUES ("2", "Tokopedia")'
    db = database_connector.Database()
    return db.run(query)

@app.route('/api/getimage/<string:imagestring>', methods = ['GET'])
def getimage(imagestring):
    success = shopee.ShopeeScraper().getimage(imagestring)
    return send_file("./static/"+imagestring+".png", mimetype='image/gif')

if __name__ == '__main__':
    app.run()