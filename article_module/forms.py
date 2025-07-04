from django import forms
from .models import Article, ArticleAuthor


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['authors_numbers', 'main_goal', 'language', 'persian_subject', 'english_subject', 'persian_Abstract',
                  'file']


class ArticleAuthorForm(forms.ModelForm):
    class Meta:
        model = ArticleAuthor
        fields = ['first_name', 'last_name', 'english_first_name', 'english_last_name', 'email', 'main_author']
