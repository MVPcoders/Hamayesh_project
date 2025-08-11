from django.contrib import admin
from . import models


class TicketAdmin(admin.ModelAdmin):
    list_display = ('user','subject','department','priority','status')
    list_editable = ('status',)

class UserAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name', 'code_meli')

admin.site.register(models.Ticket, TicketAdmin)
admin.site.register(models.User, UserAdmin)
