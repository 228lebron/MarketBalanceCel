import scrapy
from scrapy.http import FormRequest
from webscraper.spider.spider.items import ProductOfferItem


class CompelZeroDaysSpider(scrapy.Spider):
    name = 'compel_zero_days_priority_by_links'
    allowed_domains = ['www.electronshik.ru']
    start_urls = ['https://www.electronshik.ru/catalog/mikrokontrollery/KOx2',]

    def parse(self, response):
        product_urls = response.css('a.part-name::attr(href)').getall()

        for product_url in product_urls:
            yield response.follow(product_url, callback=self.parse_product)

        next_page_url = response.xpath('//*[@id="paginator"]/div/div[3]/a/@href').get()

        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse)

    def parse_product(self, response):
        item_offers = response.xpath('//table[@id="item_offers"]')
        item_data = {
            'item_id_search': item_offers.xpath('@data-item_id_search').get(),
            'query_string': item_offers.xpath('@data-query_string').get(),
            'search_brend': item_offers.xpath('@data-search_brend').get(),
            'weight': item_offers.xpath('@data-weight').get(),
            'deleted': item_offers.xpath('@data-deleted').get()
        }

        xhr_url = 'https://www.electronshik.ru/items_storage/getOffers_v2'
        xhr_data = {**item_data, 'storage': 'center', 'changed': 'true'}

        #yield FormRequest(xhr_url, formdata=xhr_data, callback=self.parse_price_table, meta={'item_data': item_data, 'url': response.url})
        yield FormRequest(
            url='https://www.electronshik.ru/items_storage/getOffers_v2',
            formdata=xhr_data,
            headers={'x-requested-with': 'XMLHttpRequest'},
            callback=self.parse_price_table,
            meta={'item_data': item_data, 'query_string': xhr_data['query_string'], 'search_brend': xhr_data['search_brend'],
                  'url': response.url}
        )

    def parse_price_table(self, response):
        item_data = response.meta['item_data']
        url = response.meta['url']

        def extract_price_and_fraction(price_element):
            price = ''.join(filter(str.isdigit, price_element.get().strip()))
            fraction = price_element.find_next_sibling('span', {'class': 'fraction'})
            fraction = fraction.text.replace(',', '') if fraction else '0'
            return float(f'{price}.{fraction}')

        dms_offers = response.css('tr.dms_offer')
        offers = [
            {
                'days': int(''.join(filter(str.isdigit, dt_selector.xpath('text()').get().strip()))),
                'prices': [extract_price_and_fraction(price_element) for price_element in offer.css('span.integer')],
                'quantity': int(offer.css('td.offer-header-avail::attr(data-qty)').get()),
            }
            for offer in dms_offers
            for dt_selector in offer.css('td.offer-header-dt')
        ]

        min_offer = min(offers, key=lambda offer: (offer['days'], min(offer['prices'])))
        min_price = min(min_offer['prices'])

        offer_item = ProductOfferItem()
        offer_item['name'] = item_data['query_string']
        offer_item['brand'] = item_data['search_brend']
        offer_item['website'] = 'ДКО Электронщик'
        offer_item['price'] = min_price
        offer_item['quantity'] = min_offer['quantity']
        offer_item['days_until_shipment'] = min_offer['days']
        offer_item['url'] = url

        yield offer_item
