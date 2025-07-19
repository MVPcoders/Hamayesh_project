from django.contrib import admin
from .models import DiscountCode


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percent', 'max_uses', 'uses', 'expiration_date', 'active']
    search_fields = ['code']
