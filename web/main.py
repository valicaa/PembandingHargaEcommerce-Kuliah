import json
from flask import Flask, send_file, jsonify, request

from controller import shopee
from controller import tokopedia

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

@app.route('/api/shopee/getimage',methods=['GET'])
def getimageshopee():
    data = request.get_json()
    shopee_handler = shopee.ShopeeScraper()
    shopee_handler.getimage(data['url'])
    return send_file("./static/"+data['url'].replace('https://cf.shopee.co.id/file/','')+".png", mimetype='image/gif')

@app.route('/api/tokopedia/getimage', methods=['GET'])
def getimagetokopedia():
    data = request.get_json()
    tokopedia_handler = tokopedia.TokopediaScraper()
    tokopedia_handler.getimage(data['url'],data['url'].replace(":","").replace("/",""))
    return send_file("./static/"+data['url'].replace(":","").replace("/","")+".png", mimetype='image/gif')

@app.route('/api/getflashsale', methods=['GET'])
def getflashsale():
    shopee_handler = shopee.ShopeeScraper()
    return jsonify(shopee_handler.getflashsale())

if __name__ == '__main__':
    app.run()