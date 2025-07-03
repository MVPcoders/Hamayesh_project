from django.contrib import admin

from article_module.models import Article, ArticleAuthor

admin.site.register(Article)
admin.site.register(ArticleAuthor)
# Register your models here.
