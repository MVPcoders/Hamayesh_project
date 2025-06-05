from django.urls import path
from . import views

urlpatterns = [
    path('request-payment/', views.send_request, name='request'),
    path('verify/', views.verify, name='verify')
]