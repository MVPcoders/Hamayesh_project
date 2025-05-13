from django.urls import path
from index_module import views

urlpatterns = [
    path('', views.index, name='index'),
]