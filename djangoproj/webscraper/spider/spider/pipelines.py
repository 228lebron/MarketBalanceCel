# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging

from djangoproj.webscraper.models import ProductOffer


logger = logging.getLogger(__name__)
class DjangoModelSavePipeline(object):
    def process_item(self, item, spider):
        try:
            model_instance = ProductOffer(**item)
            model_instance.save()
            logger.info(f'Successfully saved item: {item}')
        except Exception as e:
            logger.error(f'Error while saving item: {item}. Exception: {e}')
        return item
