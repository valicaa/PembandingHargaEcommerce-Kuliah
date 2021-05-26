from requests.models import Response
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep
import json

class TokopediaScraper():
	def __init__(self):
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66'
		}
		# headers = {
		# 	'access-control-allow-credentials': 'true',
		# 	'access-control-allow-origin': 'https://www.tokopedia.com',
		# 	'cache-control': ['no-cache', 'no-cache', 'no-store', 'must-revalidate', 'no-transform'],
		# 	'content-encoding': 'gzip',
		# 	'content-length': '16235',
		# 	'content-type': 'text/html',
		# 	'referrer-policy': 'no-referrer-when-downgrade',
		# 	'vary': 'Accept-Encoding',
		# 	'x-akamai-transformed': '9 16524 0 pmb=mTOE,1',
		# 	'x-content-type-options': 'nosniff',
		# 	'x-dns-prefetch-control': 'off',
		# 	'x-download-options': 'noopen',
		# 	'x-frame-options': 'SAMEORIGIN, ALLOW-FROM https://www.tokopedia.com',
		# 	'x-xss-protection': '1; mode=block',
		# 	'x-zeus-shell-cacheable': 'true'
		# }
		options = webdriver.ChromeOptions()
		options.add_argument('--headless')  # example
		options.add_argument('--no-sandbox')
		options.add_argument('--disable-dev-shm-usage')
		options.add_experimental_option("excludeSwitches", ["enable-automation"])
		options.add_experimental_option('useAutomationExtension', False)
		options.add_argument("--disable-blink-features=AutomationControlled")
		user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
		options.add_argument('user-agent={0}'.format(user_agent))
		# options.add_headers(headers)
		self.driver = webdriver.Remote("http://seleniumchrome:4444/wd/hub", options=options)

	def search(self,keyword):
		self.__updateurl__(keyword)
		self.driver.get(self.url)
		WebDriverWait(self.driver,30)
		items = []
		soup = self.loopThroughPages(self.driver)
		product = soup.find_all('div', class_= 'css-12sieg3')
		for i in product:
			name = soup.find('div', class_= 'css-18c4yhp').get_text()
			price = soup.find('div', class_= 'css-rhd610').get_text()
			price = price.replace('Rp ','')
			price = price.replace('.','')
			rating = soup.find('div', class_= 'css-etd83i')
			if rating:
				rating = rating.get_text()
			else:
				rating = 0
			rating_count = soup.find('div', class_= 'css-1kgbcz0')
			if rating_count:
				rating_count = rating_count.get_text()
				rating_count = rating_count.replace('Terjual ', 109)
			else:
				rating_count = 0
			link = i.a['href']
			items.append({
				'name' : str(name),
				'price' : str(price),
				'rating' : str(rating),
				'rating_count' : str(rating_count),
				'links' : str(link)
			})
		self.driver.save_screenshot('test.png')
		return product[0]

	def loopThroughPages(self, driverItem):
		i = 350
		soup = [] #Intialize empty soup array or page source
		while True:
			# sleep
			sleep(0.25)
			# Scroll down to bottom by 350 every loop
			driverItem.execute_script("window.scrollTo(0, " + str(i) + ");")
			# Get the height of the document
			new_height = driverItem.execute_script("return document.body.scrollHeight")

			i += 350  # Add i + 350 every loop

			# Check if the i is greater than document height
			if (i > new_height):
				# set the page source to using beautiful soup
				soup = BeautifulSoup(driverItem.page_source, 'lxml')
				break  # break the loop
		return soup

	# def handleToped(self,driverItem):
	# 	items = [] #Intialize empty items array
	# 	driverItem.get(self.url)
	# 	soup = self.loopThroughPages(driverItem)

	# 	if "hot" not in driverItem.current_url:
	# 		# find all product card
	# 		page = soup.find_all('div', class_="_27sG_y4O")

	# 		# loop every product card in pages
	# 		for item in page:
	# 			# find the images inside the product card div
	# 			images = item.find('div', class_="lTz_j9mr").find('img')
	# 			# print(images)
	# 			# find the names inside the product card div
	# 			name = item.find('span', class_="_1fFgipsd")

	# 			# find the price inside the product card div
	# 			price = item.find('span', class_="_2Z7a1qvz")

	# 			#remove all string from price 
	# 			price = re.sub(r"\D", "", price.get_text())

	# 			#get product link
	# 			link = item.a['href']
	# 			items.append({
	# 				"images": images['src'], 
	# 				"name": name.get_text(), 
	# 				"price": int(price), 
	# 				"links": link
	# 			})
	# 	else:
	# 		# find all product card
	# 		page = soup.find('div', id="product-results")
	# 		productCard = page.find_all('div', class_="product-card ")
	# 		for product in productCard:
	# 			image = product.a.img['src']

	# 			name = product.find('div', class_="detail__name js-ellipsis ng-binding").get_text()

	# 			link = product.a['href']

	# 			price = product.find('span', class_="detail__price ng-binding")
	# 			price = re.sub(r"\D", "", price.get_text())

	# 			items.append({
	# 				"images": image,
	# 				"name": name,
	# 				"links": link,
	# 				"price": int(price)
	# 			})
	# 	itemsSorted = sorted(items, key=lambda k: k['price'])
	# 	print(soup)
	# 	return itemsSorted

	def __updateurl__(self, keyword):
		# keyword = str(keyword).replace(" ","+")
		self.url="https://www.tokopedia.com/search?st=product&q=nintendo&navsource=home"

test = TokopediaScraper()
print(test.search('nintendo'))