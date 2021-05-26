import json
from scraper import shopee
import database_connector
import service_history

class ServiceEcommerce():
    def __init__(self):
        self.db = database_connector.Database()

    def getitems(self, keyword):
        #shopee
        history = service_history.ServiceHistory()
        items_shopee = json.loads(shopee.ShopeeScraper().search(keyword))
        for i in items_shopee:
            try:
                discount = 0
                if i['price_before_discount'] != "" :
                    discount = (int(i['price_before_discount']) - int(i['price'])) / int(i['price_before_discount']) * 100
                link = i['names']
                link = link.replace(" ", "-")
                link = "https://shopee.co.id/" +link + "-i." + str(i['shopid']) + '.' + str(i['itemid'])
                query = 'REPLACE INTO barang VALUES (' + str(i['itemid']) + ', ' + '1' + ', ' + str(i['categoryid']) + ', ' + str(i['price']) + ', ' + str(discount) + ', ' + str(i['stock']) + ', ' + str(i['rating']) + ', ' + str(i['rating_count']) + ', ' + '"' + str(i['names']) + '"' + ', ' + '"' +  str(i['image']) + '"' + ', ' + '"' + link + '"' + ')'
                print(self.db.run(query))
                # print(i['itemid'])
                history.updatehistory(1,i['itemid'])
            except:
                print("error")
        return "query"

# test = ServiceEcommerce()
# test.getitems('nintendo switch')
