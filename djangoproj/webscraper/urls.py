from django.urls import path

from .views import price_difference, product_analysis, scrap


urlpatterns = [
    path('price_diff/<str:name>/<str:brand>/', price_difference, name='price_difference'),
    path('product_analysis/<str:product_name>/<str:product_brand>/', product_analysis, name='product_analysis'),
    path('scrap/', scrap, name='scrap')
]