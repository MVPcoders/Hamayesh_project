from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('persian_subject', 'is_visited', 'is_coached', 'is_accepted', 'is_paid', 'submit_date','need_correction','is_corrected')
    list_editable = ('is_paid', 'is_visited', 'is_coached', 'is_accepted')
    list_filter = ('is_visited', 'is_coached', 'is_accepted', 'is_paid', 'need_correction', 'is_corrected')
    search_fields = ('persian_subject', 'english_subject', 'main_goal')
    ordering = ('-submit_date',)
    readonly_fields = ('submit_date',)


admin.site.register(Article, ArticleAdmin)
