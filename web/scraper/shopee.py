import json
import requests

class ShopeeScraper():
    def __init__(self):
        self.keyword = ""
        self.limit = str(20)
        self.order = "desc"
        self.page_type = "search"
        self.url="https://shopee.co.id/api/v4/search_items/?by=relevancy&keyword="+self.keyword+"&limit="+self.limit+"&order="+self.order+"&page_type="+self.page_type
    
    def search(self, keyword):
        self.keyword = keyword
        self.__updateurl__()
        pageheaders = {}
        pageheaders["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
        html = requests.get(self.url,headers = pageheaders).json()

        itemid = []
        shopid = []
        category = []
        price = []
        pricebeforedisc = []
        stock = []
        names = []

        for i in range(0,len(html['items'])):
            itemid.append(html['items'][i]['itemid'])
            shopid.append(html['items'][i]['shopid'])
            category.append(html['items'][i]['catid'])
            price.append(html['items'][i]['price'])
            pricebeforedisc.append(html['items'][i]['price_before_discount'])
            stock.append(html['items'][i]['stock'])
            names.append(html['items'][i]['name'])
        items = list(zip(names,itemid,shopid,category,price,pricebeforedisc,stock))
        return items
            

    def finditem(self,itemid,shopid):
        itemurl = "https://shopee.co.id/api/v2/item/get?itemid="+itemid+"&shopid="+shopid
        client = urllib.request.urlopen(itemurl)
        html = json.loads(client.read())
        client.close()
        return ""
        
    def __updateurl__(self):
        self.url="https://shopee.co.id/api/v2/search_items/?by=relevancy&keyword="+self.keyword+"&limit="+self.limit+"&order="+self.order+"&page_type="+self.page_type

test = ShopeeScraper()
print(test.search("samsung"))