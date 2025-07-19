from django.db import models
from account_module.models import User
from django.utils import timezone
import random
import string


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


class DiscountCode(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name="کد تخفیف")
    discount_percent = models.PositiveIntegerField(default=0, verbose_name="درصد تخفیف")
    max_uses = models.PositiveIntegerField(default=1, verbose_name="حداکثر استفاده")
    uses = models.PositiveIntegerField(default=0, verbose_name="تعداد استفاده شده")
    expiration_date = models.DateTimeField(verbose_name="تاریخ انقضا",null=True, blank=True)
    active = models.BooleanField(default=True, verbose_name="فعال")

    def __str__(self):
        return self.code

    def is_valid(self, user=None):
        if not self.active:
            return False
        if self.uses >= self.max_uses:
            return False
        return True

    def use_code(self):
        self.uses += 1
        if self.uses >= self.max_uses:
            self.active = False
        self.save()
