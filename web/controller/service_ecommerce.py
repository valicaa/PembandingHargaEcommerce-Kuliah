import json
from scraper import shopee
from scraper import tokopedia
import database_connector

class ServiceEcommerce():
    def __init__(self):
        self.db = database_connector.Database()

    def getitems(self, keyword):
        items = []

        #shopee
        items_shopee = json.loads(shopee.ShopeeScraper().search(keyword))

        #append shopee
        items.append(items_shopee)

        # for i in items_shopee:
        #     try:
        #         discount = 0
        #         if i['price_before_discount'] != "" :
        #             discount = 100 - (int(i['price'])/int(i['price_before_discount']))*100
        #         link = i['names']
        #         link = link.replace(" ", "-")
        #         link = "https://shopee.co.id/" +link + "-i." + str(i['shopid']) + '.' + str(i['itemid'])
        #         query = 'REPLACE INTO barang VALUES (' + str(1 + i['itemid']) + ', ' + '1' + ', ' + str(i['categoryid']) + ', ' + str(i['price']) + ', ' + str(discount) + ', ' + str(i['stock']) + ', ' + str(i['rating']) + ', ' + str(i['rating_count']) + ', ' + '"' + str(i['names']) + '"' + ', ' + '"' +  str(i['image']) + '"' + ', ' + '"' + link + '"' + ')'
        #         print(self.db.run(query))
        #         # print(i['itemid'])
        #         history.updatehistory(1,i['itemid'])
        #     except:
        #         print("error")

        #tokopedia
        items_toped = json.loads(tokopedia.TokopediaScraper().search(keyword))
        items.append(items_toped)

        return items

# test = ServiceEcommerce()
# print(test.getitems('nintendo switch'))
