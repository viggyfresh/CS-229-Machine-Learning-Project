from bs4 import BeautifulSoup
import requests
import os
import gevent

product_names = []
product_urls = []
img_urls = []


def main():
	os.chdir('./images')
	for i in range (0, 1):
		url = "http://www.zappos.com/mens-sneakers-athletic-shoes~dA?zfcTest=sis%3A0#!/men-sneakers-athletic-shoes-page2/CK_XARC81wHAAQLiAgMBGAI.zso?p=" + str(i) + "0&s=recentSalesStyle/desc/"
		text = get_page(url)
		get_product_list(text)
	print product_urls
	for url in product_urls:
		product_page = get_page(url)
		parse_product_page(product_page)
	print img_urls
	batch_save_images()


def get_page(url):
	response = requests.get(url)
	return response.text

def get_product_list(text):
	BS = BeautifulSoup(text)
	for product in BS.find_all("a", class_="product"):
		product_urls.append("http://www.zappos.com" + product.get("href"))

def parse_product_page(text):
	BS = BeautifulSoup(text)
	img_urls.append("http://www.zappos.com" + BS.find("a", id="angle-3").get("href"))
	product_names.append(BS.title.string.split(' - ')[0].replace("/", "-"))

def save_img(url, i):
   	resp = requests.get(url)
   	fout = open(str(i) + "-" + str(product_names[i]) + ".jpg", "wb")
   	fout.write(resp.content)
   	fout.close()

def batch_save_images():
	threads = [gevent.spawn(save_img, img_urls[i], i) for i in xrange(len(img_urls))]
	gevent.joinall(threads)

main()