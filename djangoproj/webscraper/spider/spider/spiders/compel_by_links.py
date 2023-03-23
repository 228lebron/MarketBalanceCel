import scrapy
#from webscraper.spider.spider.items import ProductItem


class ExampleSpider(scrapy.Spider):
    name = 'example_spider'
    allowed_domains = ['electronshik.ru']
    start_urls = ['https://www.electronshik.ru/item/JRC/NJM4558D']

    def parse(self, response):
        #my_item = ProductItem()
        #my_item['name'] = response.css('h2::text').get()
        pass
        #yield my_item