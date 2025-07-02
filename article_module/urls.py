# from django.urls import path
# from .views import aricle
#
# urlpatterns = [
#     path('new-article/', aricle, name='new_article'),
# ]
from django.urls import path
from .views import submit_article

urlpatterns = [
    path('new-article/', submit_article, name='new_article'),
]
