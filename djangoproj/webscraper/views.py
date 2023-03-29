from django.shortcuts import render
from django.db.models import F
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET

from .models import ProductOffer
from .product_analysis import average_price, lowest_price, fastest_shipping
from .utils import get_plot, get_prices_history_data, get_price_data_d

from . import tasks


def scrap(request):
    tasks.run_scrapy_spider.delay()
    return HttpResponse('Задача иди нахуй')



@require_GET
def price_difference(request, name, brand):
    offers = ProductOffer.objects.filter(name=name, brand=brand)
    print(offers)
    data = {}
    for offer in offers:
        other_offers = ProductOffer.objects.filter(
            name=name, brand=brand, ).exclude(pk=offer.pk)
        if other_offers.exists():
            other_offer = other_offers.first()
            price_difference = other_offer.price - offer.price
            percentage_difference = (
                (price_difference / offer.price) * 100 if offer.price else 0
            )
            data[offer.website] = {
                'price': offer.price,
                "price_difference": price_difference,
                "percentage_difference": percentage_difference,
            }
    return JsonResponse(data)


def product_analysis(request, product_name, product_brand):
    avg_price = average_price(product_name)
    best_price_offer = lowest_price(product_name)

    prices_d, dates_d = get_price_data_d(product_name, product_brand)
    chart = get_plot(dates_d, prices_d, 'График цен')
    best_shipping_offer = fastest_shipping(product_name)

    context = {
        'product_name': product_name,
        'product_brand': product_brand,
        'avg_price': avg_price,
        'best_price_offer': best_price_offer,
        'best_shipping_offer': best_shipping_offer,
        'graph': chart,

    }

    return render(request, 'product_analysis.html', context)