from celery import shared_task
from billiard import Process
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from .spider.spider.spiders.compel_zero_days_priority import CompelZeroDaysSpider


def _run_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl(CompelZeroDaysSpider)
    process.start()

@shared_task
def run_scrapy_spider():
    process = Process(target=_run_spider)
    process.start()
    process.join()
