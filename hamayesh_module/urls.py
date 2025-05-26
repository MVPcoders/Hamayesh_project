from django.urls import path
from hamayesh_module import views

urlpatterns = [
    path('', views.HamayeshModule , name='hamayesh-page'),
]