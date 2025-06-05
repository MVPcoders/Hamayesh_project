from django.db import models

class TotalSales(models.Model):
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    last_reset = models.DateField(auto_now=True)

    def reset_sales(self):
        self.total_amount = 0
        self.save()
