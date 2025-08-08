from django.urls import path
from index_module import views

urlpatterns = [
    path('', views.index, name='index'),
    path('404/',views.page_not_found,name='404_page')
]