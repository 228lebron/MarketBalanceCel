import base64
from io import BytesIO
import matplotlib.pyplot as plt
from .models import ProductOffer


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(x, y, lable):
    plt.switch_backend('AGG')
    plt.figure(figsize=(9,5))
    plt.title(lable, fontsize=16, fontweight='bold')
    for site, y in y.items():
        plt.plot(x[site], y, label=site, linewidth=2, marker='o', markersize=6)
    plt.legend(loc='best', fontsize=12)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_prices_history_data(product):
    offers = ProductOffer.objects.filter(name=product_name).order_by('timestamp')
    competitors = offers.values_list('website', flat=True).distinct()

def get_price_data_d(product, brand):
    offers = ProductOffer.objects.filter(name=product, brand=brand)
    prices = {}
    dates = {}
    lead_times = {}
    quantity = {}
    for offer in offers.order_by('timestamp'):
        supplier = offer.website
        if supplier not in prices:
            prices[supplier] = []
            dates[supplier] = []
            lead_times[supplier] = []
            quantity[supplier] = []
        prices[supplier].append(offer.price)
        dates[supplier].append(offer.timestamp.date())
        lead_times[supplier].append(offer.days_until_shipment)
        quantity[supplier].append(offer.quantity)
    return prices, dates