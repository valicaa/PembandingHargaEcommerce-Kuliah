from flask import Flask, send_file, jsonify, request

from controller import shopee
from controller import tokopedia

import urllib.request

app = Flask(__name__, static_url_path='/static')

@app.route('/api/search/<string:keyword>',methods=['GET'])
def searchproduct(keyword):
    shopee_handler = shopee.ShopeeScraper()
    tokopedia_handler = tokopedia.TokopediaScraper()
    items_shopee = shopee_handler.search(keyword)
    items_tokopedia = tokopedia_handler.search(keyword)
    items = []
    items.append(items_shopee)
    items.append(items_tokopedia)
    return jsonify(items)

@app.route('/api/getimage/shopee/<string:imageurl>',methods=['GET'])
def getimageshopee(imageurl):
    shopee_handler = shopee.ShopeeScraper()
    shopee_handler.getimage(imageurl)
    return send_file("./static/"+imageurl+".png", mimetype='image/gif')

@app.route('/api/getimage/tokopedia', methods=['GET'])
def getimagetokopedia():
    data = request.get_json()
    tokopedia_handler = tokopedia.TokopediaScraper()
    tokopedia_handler.getimage(data['url'],data['url'].replace(":","").replace("/",""))
    return send_file("./static/"+data['url'].replace(":","").replace("/","")+".png", mimetype='image/gif')

# @app.route('/api/getimage/<string:imagestring>', methods = ['GET'])
# def getimage(imagestring):
#     success = shopee.ShopeeScraper().getimage(imagestring)
#     return send_file("./static/"+imagestring+".png", mimetype='image/gif')

if __name__ == '__main__':
    app.run()