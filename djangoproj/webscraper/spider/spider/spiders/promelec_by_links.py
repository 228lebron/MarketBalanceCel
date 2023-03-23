import scrapy
from webscraper.spider.spider.items import ProductOfferItem

class PromelecByLinksSpider(scrapy.Spider):
    name = 'promelec_by_links'
    allowed_domains = ['www.promelec.ru']
    start_urls = ['https://www.promelec.ru/catalog/1/11/2779/?page=1']

    def parse(self, response):
        items = response.css('div.table-list__item')
        for item in items:
            if item.css('span.table-list__counter::text').re_first('\d+') is not None and int(
                    item.css('span.table-list__counter::text').re_first('\d+')) > 0:

                product_name = item.css('a.product-preview__title::attr(title)').get()
                brand = item.css('span.product-preview__code a::text').get()
                qty = int(item.css('span.table-list__counter::text').re_first('\d+'))
                price = float(item.css('span.table-list__price::text').re_first('\d+[\.,]?\d*').replace(',','.'))
                url = item.css('a.product-preview__title::attr(href)').get()
                print(product_name, brand, qty, price, url)

                offer_item = ProductOfferItem()
                offer_item['name'] = product_name
                offer_item['brand'] = brand
                offer_item['website'] = 'Промэлектроника'
                offer_item['price'] = price
                offer_item['quantity'] = qty
                offer_item['days_until_shipment'] = 0
                offer_item['url'] = url

                yield offer_item


        next_page_url = response.css('a.paging-next__link::attr(href)').get()
        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)
