from django.db.models import Avg
from django.conf import settings
from .models import ProductOffer
import matplotlib.pyplot as plt
import os


def average_price(product_name):
    return ProductOffer.objects.filter(name=product_name).aggregate(Avg('price'))


def lowest_price(product_name):
    return ProductOffer.objects.filter(name=product_name).order_by('price').first()


def price_history_chart(product_name):
    offers = ProductOffer.objects.filter(name=product_name).order_by('timestamp')
    competitors = offers.values_list('website', flat=True).distinct()

    for competitor in competitors:
        competitor_offers = offers.filter(website=competitor)
        timestamps = [offer.timestamp for offer in competitor_offers]
        prices = [offer.price for offer in competitor_offers]
        output_file = os.path.join(settings.MEDIA_ROOT, f'price_history_{product_name}.png')
        plt.plot(timestamps, prices, label=competitor)
        plt.savefig(output_file)

    plt.title(f'Price History of {product_name}')
    plt.xlabel('Timestamp')
    plt.ylabel('Price')
    plt.legend()
    plt.savefig(f'price_history_{product_name}.png')


def fastest_shipping(product_name):
    return ProductOffer.objects.filter(name=product_name).order_by('days_until_shipment').first()