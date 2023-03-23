from scrapy_djangoitem import DjangoItem
from webscraper.models import ProductOffer


class ProductOfferItem(DjangoItem):
    django_model = ProductOffer
