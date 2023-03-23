from django.db.models import F
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import ProductOffer


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
