from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
#from .spider.spider.spiders.compel_zero_days_priority import CompelZeroDaysSpider

from ...spider.spider.spiders.compel_zero_days_priority import CompelZeroDaysSpider

class Command(BaseCommand):
    help = 'Run the Scrapy spider'

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())
        process.crawl(CompelZeroDaysSpider)
        process.start()