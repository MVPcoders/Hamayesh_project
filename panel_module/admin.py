from django.contrib import admin
from order_module.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'payment_date', 'is_successful')
    list_filter = ('is_successful', 'payment_date')
    search_fields = ('user__username', 'transaction_id')
