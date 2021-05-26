import time

import redis
from flask import Flask, render_template, send_file

from controller import service_ecommerce 

app = Flask(__name__, static_url_path='/static')
cache = redis.Redis(host='redis', port=6379)

@app.route('/')
def hello():
    return 'Hello World Its me'

@app.route('/api/search/<string:keyword>',methods=['GET'])
def searchproduct(keyword):
    ecommerce = service_ecommerce.ServiceEcommerce()
    items = ecommerce.getitems(keyword)
    return items

@app.route('/api/getimage/<string:imagestring>', methods = ['GET'])
def getimage(imagestring):
    success = shopee.ShopeeScraper().getimage(imagestring)
    return send_file("./static/"+imagestring+".png", mimetype='image/gif')

if __name__ == '__main__':
    app.run()