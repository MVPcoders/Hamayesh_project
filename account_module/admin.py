from django.contrib import admin
from . import models


class TicketAdmin(admin.ModelAdmin):
    list_display = ('user','subject','department','priority','status')
    list_editable = ('status',)


admin.site.register(models.Ticket, TicketAdmin)
admin.site.register(models.User)
