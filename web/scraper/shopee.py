import json
import requests
from io import BytesIO

class ShopeeScraper():
    def __init__(self):
        self.keyword = ""
        self.limit = str(20)
        self.order = "desc"
        self.page_type = "search"
        self.url="https://shopee.co.id/api/v4/search_items/?by=relevancy&keyword="+self.keyword+"&limit="+self.limit+"&order="+self.order+"&page_type="+self.page_type
        self.headers = {
            "accept-encoding": "gzip, deflate, br",
            "content-type": "application/json",
            "if-none-match": "55b03-1ae7d4aa7c47753a96c0ade3a9ea8b35",
            "origin": "https://shopee.co.id",
            "referer": "https://shopee.co.id/asusofficialshop",
            "x-api-source": "pc",
            "x-csrftoken": "8XtQ7bHlv09rlx5U4NPN6rmavFn7MvTO",
            "x-requested-with": "XMLHttpRequest",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "cookie": 'SPC_IA=-1; SPC_EC=-; SPC_F=QpolQhTSikpnxRXO6T4RjIW8ZGHNBmBn; REC_T_ID=ac80cdde-0e7d-11e9-a8c2-3c15fb3af585; SPC_T_ID="e4t1VmH0VKB0NajA1BrHaDQlFRwWjTZT7o83rrHW+p16sTf1NJK7ksWWDicCTPq8CVO/S8sxnw25gNR0DLQz3cv7U3EQle9Z9ereUnPityQ="; SPC_SI=k2en4gw50emawx5fjaawd3fnb5o5gu0w; SPC_U=-; SPC_T_IV="in3vKQSBLhXzeTaGwMInvg=="; _gcl_au=1.1.557205539.1546426854; csrftoken=8XtQ7bHlv09rlx5U4NPN6rmavFn7MvTO; welcomePkgShown=true; bannerShown=true; _ga=GA1.3.472488305.1546426857; _gid=GA1.3.1348013297.1546426857; _fbp=fb.2.1546436170115.11466858'
        }
    
    def search(self, keyword):
        self.keyword = keyword
        self.__updateurl__()
        html = requests.get(self.url,headers = self.headers).json()

        itemid = []
        shopid = []
        category = []
        price = []
        pricebeforedisc = []
        stock = []
        names = []
        image = []

        #print(html)
        for i in range(0,len(html['items'])):
            itemid.append(html['items'][i]['itemid'])
            shopid.append(html['items'][i]['shopid'])
            category.append(html['items'][i]['catid'])
            price.append(html['items'][i]['price'])
            pricebeforedisc.append(html['items'][i]['price_before_discount'])
            stock.append(html['items'][i]['stock'])
            names.append(html['items'][i]['name'])
            image.append(html['items'][i]['image'])
        items = list(zip(names,itemid,shopid,category,price,pricebeforedisc,stock,image))
        return items

    # def finditem(self,itemid,shopid):
    #     itemurl = "https://shopee.co.id/api/v2/item/get?itemid="+itemid+"&shopid="+shopid
    #     client = urllib.request.urlopen(itemurl, headers=self.headers)
    #     html = json.loads(client.read())
    #     client.close()
    #     return ""
        
    def __updateurl__(self):
        self.url="https://shopee.co.id/api/v2/search_items/?by=relevancy&keyword="+self.keyword+"&limit="+self.limit+"&order="+self.order+"&page_type="+self.page_type

    def getimage(self, imagestring):
        url = "https://cf.shopee.co.id/file/" + imagestring
        response = requests.get(url, headers = self.headers)
        try:
            file=open("./static/"+imagestring+".png")
            file.close()
            return True
        except:
            file = open("./static/"+imagestring+".png","wb")
            if(response.content):
                file.write(response.content)
                file.close()
            else:
                file.close()
            return False

# test = ShopeeScraper()
# print(test.getimage("2f276cef5fd9ff524bcd03027acfee8c"))