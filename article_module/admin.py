from django.contrib import admin

from article_module.models import Article


class ArticleAdmin(admin.ModelAdmin):
    readonly_fields = ['submit_date']
admin.site.register(Article, ArticleAdmin)
# Register your models here.
