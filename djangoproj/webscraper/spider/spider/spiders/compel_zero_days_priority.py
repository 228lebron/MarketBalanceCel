import scrapy
import requests
from bs4 import BeautifulSoup
import re
from webscraper.spider.spider.items import ProductOfferItem
from webscraper.spider.spider.utils import map_brand_name


class CompelZeroDaysSpider(scrapy.Spider):
    name = 'compel_zero_days_priority'
    allowed_domains = ['www.electronshik.ru']
    start_urls = ['https://www.electronshik.ru/catalog/mikrokontrollery/KOx2',]

    def parse(self, response):
        product_urls = response.css('a.part-name::attr(href)').getall()

        for product_url in product_urls:
            yield scrapy.Request(response.urljoin(product_url), callback=self.parse_product)

        next_page_url = response.xpath('//*[@id="paginator"]/div/div[3]/a/@href').get()

        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)

    def parse_product(self, response):
        item_offers = response.xpath('//table[@id="item_offers"]')
        item_id_search = item_offers.xpath('@data-item_id_search').get()
        query_string = item_offers.xpath('@data-query_string').get()
        search_brend = item_offers.xpath('@data-search_brend').get()
        weight = item_offers.xpath('@data-weight').get()
        deleted = item_offers.xpath('@data-deleted').get()

        cookies = {
            'ELECTRO': 'ph1q1pfe869irt5nqh3kp27jq4',
            'dimension7': 'ax1',
            '_ym_uid': '1679378866694971231',
            '_ym_d': '1679378866',
            '_ym_isad': '2',
            '_gcl_au': '1.1.970854413.1679378868',
            '_ga': 'GA1.2.1647783015.1679378868',
            '_gid': 'GA1.2.855640701.1679378868',
            '_ym_visorc': 'w',
        }

        headers = {
            'authority': 'www.electronshik.ru',
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.electronshik.ru',
            'referer': response.url,  # Use the current response URL instead of a hardcoded one
            'sec-ch-ua': '"Not=A?Brand";v="8", "Chromium";v="110", "Opera";v="96"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0',
            'x-requested-with': 'XMLHttpRequest',
        }

        # make the second request
        xhr_url = 'https://www.electronshik.ru/items_storage/getOffers_v2'
        xhr_data = {
            'storage': 'center',
            'item_id_search': item_id_search,
            'query_string': query_string,
            'search_brend': search_brend,
            'weight': weight,
            'deleted': deleted,
            'changed': 'true'
        }

        print('Making XHR request:', xhr_url)
        price_table_response = requests.post('https://www.electronshik.ru/items_storage/getOffers_v2', cookies=cookies,
                                 headers=headers, data=xhr_data)

        def collect_fraction(price_element):
            fraction_element = price_element.find_next_sibling('span', {'class': 'fraction'})
            if fraction_element is not None:
                return fraction_element.text.replace(',','')
            else:
                return 0

        soup = BeautifulSoup(price_table_response.content, features='lxml')
        dms_offers = soup.find_all('tr', {'class': 'dms_offer'})

        # Initialize variables to keep track of the lowest price and the number of days until shipment
        lowest_price = None
        lowest_price_qty = None
        days = None

        for offer in dms_offers:
            days_until_shipment_element = offer.find('td', {'class': 'offer-header-dt'}).text.strip()
            days_until_shipment = int(''.join(filter(str.isdigit, days_until_shipment_element)))
            price_elements = offer.find_all('span', {'class': 'integer'})

            for price_element in price_elements:
                if price_element is not None:
                    price = re.sub(r'\D', '', price_element.text)
                    fraction = collect_fraction(price_element)
                    price = float(price + '.' + fraction)
                    qty_td = offer.find('td', {'class': 'offer-header-avail'})

                    if (days == 0 or days is None) and days_until_shipment == 0:
                        if lowest_price is None or price < lowest_price:
                            lowest_price = price
                            lowest_price_qty = int(qty_td['data-qty'])
                            days = days_until_shipment
                    elif days is None or days_until_shipment < days:
                        lowest_price = price
                        lowest_price_qty = int(qty_td['data-qty'])
                        days = days_until_shipment

        offer_item = ProductOfferItem()
        offer_item['name'] = query_string
        offer_item['brand'] = map_brand_name(search_brend)
        offer_item['website'] = 'Compel'
        offer_item['price'] = lowest_price
        offer_item['quantity'] = lowest_price_qty
        offer_item['days_until_shipment'] = days
        offer_item['url'] = response.url

        yield offer_item

