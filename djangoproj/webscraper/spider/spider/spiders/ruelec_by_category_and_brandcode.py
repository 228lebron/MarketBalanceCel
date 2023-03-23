import scrapy
import requests
from bs4 import BeautifulSoup
import re
from webscraper.spider.spider.items import ProductOfferItem

class RuelecByCategoryAndBrandcodeSpider(scrapy.Spider):
    name = 'ruelec_by_category_and_brandcode'
    allowed_domains = ['ruelectronics.com']
    start_urls = ['https://ruelectronics.com/mikroshemy/kontrollery/']

    def parse(self, response):

        cookies = {
            'PHPSESSID': '07236610c3a73995e4ab7bf9b712d76a',
            'default': '2c19cde4b4dbd42700b8cf1b7cf7814c',
            'language': 'ru-ru',
            'currency': 'RUB',
            'a077d4058c7604a345cdd79324955f9d': '9793b6cfe40f065fb4247317bb1ea9eb',
            '_gcl_au': '1.1.571774269.1679553087',
            '_gid': 'GA1.2.484820107.1679553087',
            '_ym_uid': '1679553087262185939',
            '_ym_d': '1679553087',
            '_ym_isad': '2',
            '_ym_visorc': 'w',
            '_gat_gtag_UA_133172054_52': '1',
            'view_prod': '%7B%220%22%3A0%2C%222%22%3A32175%2C%224%22%3A0%7D',
            '_ga_SNS4NGX11Z': 'GS1.1.1679565728.3.1.1679565820.0.0.0',
            '_ga': 'GA1.2.1090592071.1679553087',
        }

        headers = {
            'authority': 'ruelectronics.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            # 'cookie': 'PHPSESSID=07236610c3a73995e4ab7bf9b712d76a; default=2c19cde4b4dbd42700b8cf1b7cf7814c; language=ru-ru; currency=RUB; a077d4058c7604a345cdd79324955f9d=9793b6cfe40f065fb4247317bb1ea9eb; _gcl_au=1.1.571774269.1679553087; _gid=GA1.2.484820107.1679553087; _ym_uid=1679553087262185939; _ym_d=1679553087; _ym_isad=2; _ym_visorc=w; _gat_gtag_UA_133172054_52=1; view_prod=%7B%220%22%3A0%2C%222%22%3A32175%2C%224%22%3A0%7D; _ga_SNS4NGX11Z=GS1.1.1679565728.3.1.1679565820.0.0.0; _ga=GA1.2.1090592071.1679553087',
            'origin': 'https://ruelectronics.com',
            'referer': response.url,
            'sec-ch-ua': '"Not=A?Brand";v="8", "Chromium";v="110", "Opera";v="96"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0',
        }

        data = {
            'propertyManufacturer[]': '504',
        }

        print('Making XHR request')

        xhr_response = requests.post('https://ruelectronics.com/mikroshemy/kontrollery/', cookies=cookies,
                                             headers=headers, data=data)

        soup = BeautifulSoup(xhr_response.content, features='lxml')
        products = soup.find_all('div', {'class': 'b-product-list__item'})
        for product in products:

            item_prices = product.find_all('div', {'class': 'item-price'})
            if len(item_prices) > 2:
                product_name = product.find('a', {'class': 'h4'}).text.split(',')[0].strip()
                brand = product.find('a', {'class': 'h4'}).text.split(',')[1].split(' ')[-1].strip()
                bulk_price_str = float(item_prices[1].find('b').text.replace(' руб./шт.','').strip())
                quantity = int(product.find('div', {'class': 'amount in-stock'}).find('span').text)

                if product_name and brand and bulk_price_str and quantity:
                    offer_item = ProductOfferItem()
                    offer_item['name'] = product_name
                    offer_item['brand'] = brand
                    offer_item['website'] = 'RuElectronics'
                    offer_item['price'] = bulk_price_str
                    offer_item['quantity'] = quantity
                    offer_item['days_until_shipment'] = 0
                    offer_item['url'] = product.find('a', {'class': 'h4'})['href']
                    yield offer_item