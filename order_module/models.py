from django.db import models
from account_module.models import User


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    payment_date = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['-payment_date']

    def __str__(self):
        return f"{self.amount} - {self.payment_date.strftime('%Y-%m-%d')}"

