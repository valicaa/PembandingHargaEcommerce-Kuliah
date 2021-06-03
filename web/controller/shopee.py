import json
import requests
from io import BytesIO
import urllib.request

class ShopeeScraper():
    def __init__(self):
        self.keyword = ""
        self.url="https://shopee.co.id/api/v4/search/search_items?by=relevancy&keyword="+self.keyword+"&limit=50&newest=0&order=desc&page_type=search&version=2"
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
        html = requests.get(self.url, headers = self.headers).json()

        # itemid = []
        # shopid = []
        # category = []
        # price = []
        # pricebeforedisc = []
        # stock = []
        # names = []
        # image = []

        #print(html)
        mylist = []
        discount = 0
        if str(html['items'][0]['item_basic']['price_before_discount'])[:-5] != "" :
            discount = 100 - ((int(str(html['items'][0]['item_basic']['price'])[:-5])/int(str(html['items'][0]['item_basic']['price_before_discount'])[:-5]))*100)

        updateitem = {
            'names' : html['items'][0]['item_basic']['name'],
            'itemid' : html['items'][0]['item_basic']['itemid'],
            'shopid' : html['items'][0]['item_basic']['shopid'],
            #'categoryid' : html['items'][0]['item_basic']['catid'],
            'price' : int(str(html['items'][0]['item_basic']['price'])[:-5]),
            'discount' : str(discount),
            'price_before_discount' : str(html['items'][0]['item_basic']['price_before_discount'])[:-5],
            #'stock' : html['items'][0]['item_basic']['stock'],
            'image' : html['items'][0]['item_basic']['image'],
            'rating' : html['items'][0]['item_basic']['item_rating']['rating_star'],
            'rating_count' : html['items'][0]['item_basic']['item_rating']['rating_count'][0],
            'link' : "https://shopee.co.id/" + str(html['items'][0]['item_basic']['name']).replace(" ","-") + "-i." + str(html['items'][0]['item_basic']['shopid']) + '.' + str(html['items'][0]['item_basic']['itemid']),
            'ecommerce' : 'shopee'
        }
        mylist.append(updateitem)

        for i in range(1,len(html['items'])):
            # itemid.append(html['items'][i]['itemid'])
            # shopid.append(html['items'][i]['shopid'])
            # category.append(html['items'][i]['catid'])
            # price.append(str(html['items'][i]['price'])[:-5])
            # pricebeforedisc.append(str(html['items'][i]['price_before_discount'])[:-5])
            # stock.append(html['items'][i]['stock'])
            # names.append(html['items'][i]['name'])
            # image.append(html['items'][i]['image'])
            discount = 0
            if str(html['items'][i]['item_basic']['price_before_discount'])[:-5] != "" :
                discount = 100 - ((int(str(html['items'][i]['item_basic']['price'])[:-5])/int(str(html['items'][i]['item_basic']['price_before_discount'])[:-5]))*100)
            updateitem = {
                'names' : html['items'][i]['item_basic']['name'],
                'itemid' : html['items'][i]['item_basic']['itemid'],
                'shopid' : html['items'][i]['item_basic']['shopid'],
                #'categoryid' : html['items'][i]['item_basic']['catid'],
                'price' : int(str(html['items'][i]['item_basic']['price'])[:-5]),
                'discount' : str(discount),
                'price_before_discount' : str(html['items'][i]['item_basic']['price_before_discount'])[:-5],
                #'stock' : html['items'][i]['item_basic']['stock'],
                'image' : html['items'][i]['item_basic']['image'],
                'rating' : html['items'][i]['item_basic']['item_rating']['rating_star'],
                'rating_count' : html['items'][i]['item_basic']['item_rating']['rating_count'][0],
                'link' : "https://shopee.co.id/" + str(html['items'][i]['item_basic']['name']).replace(" ","-") + "-i." + str(html['items'][i]['item_basic']['shopid']) + '.' + str(html['items'][i]['item_basic']['itemid']),
                'ecommerce' : 'shopee'
            }
            mylist.append(updateitem)
        #items = list(zip(names,itemid,shopid,category,price,pricebeforedisc,stock,image)
        return json.dumps(mylist)

    # def finditem(self,itemid,shopid):
    #     itemurl = "https://shopee.co.id/api/v2/item/get?itemid="+itemid+"&shopid="+shopid
    #     client = urllib.request.urlopen(itemurl, headers=self.headers)
    #     html = json.loads(client.read())
    #     client.close()
    #     return ""
        
    def __updateurl__(self):
        self.url="https://shopee.co.id/api/v4/search/search_items?by=relevancy&keyword="+self.keyword+"&limit=50&newest=0&order=desc&page_type=search&version=2"

    def getimage(self, imagestring):
        url = "https://cf.shopee.co.id/file/" + imagestring
        #response = requests.get(url, headers = self.headers)
        return urllib.request.urlretrieve(url, "static/"+imagestring+".png")
        # try:
        #     file=open("./static/"+imagestring+".png")
        #     file.close()
        #     return True
        # except:
        #     if(response.content):
        #         file = open("./static/"+imagestring+".png","wb")
        #         file.write(response.content)
        #         file.close()
        #         return True
        #     return False

    def getproductdetail(self,itemid,shopid):
        url = "https://shopee.co.id/api/v2/item/get?itemid="+str(itemid)+"&shopid="+str(shopid)
        response = requests.get(url, headers = self.headers).json()
        return response

test = ShopeeScraper()
print(test.getproductdetail(7383182794,46956772))