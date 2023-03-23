from django.db import models


class ProductOffer(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    days_until_shipment = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    url = models.URLField()

    def __str__(self):
        return f"{self.name} ({self.website}): price={self.price}, quantity={self.quantity}"
