from django.urls import path
from . import views

urlpatterns = [
    path('', views.pay, name='payment'),
    path('callback-paytest/', views.callback_gateway_view, name='call'),
    path('request-payment/<int:article_id>', views.send_request, name='request'),
    path('verify/', views.verify, name='verify')
]