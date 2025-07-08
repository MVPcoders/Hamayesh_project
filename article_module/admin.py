from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('persian_subject', 'is_visited', 'is_coached', 'is_accepted', 'is_paid', 'submit_date')
    list_editable = ('is_paid', 'is_visited', 'is_coached', 'is_accepted')
    list_filter = ('is_visited', 'is_coached', 'is_accepted', 'is_paid')
    search_fields = ('persian_subject', 'english_subject', 'main_goal')
    ordering = ('-submit_date',)
    fields = ('user', 'authors_numbers', 'authors_info', 'main_goal', 'language',
              'persian_subject', 'english_subject', 'article_abstract', 'file',
              'is_visited', 'is_coached', 'is_accepted', 'is_paid', 'submit_date')
    readonly_fields = ('submit_date',)  # Make submit_date read-only


admin.site.register(Article, ArticleAdmin)
