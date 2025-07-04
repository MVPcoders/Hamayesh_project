from django.db import models

from django.db import models


class Sale(models.Model):
    price = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.price

# Create your models here.
