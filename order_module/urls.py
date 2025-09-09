# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('', views.pay, name='payment'),
#     # path("zibal/request/<int:article_id>/", views.send_request_view, name="request"),
#     # path("zibal/verify/", views.verify_view, name="verify"),
#     path('request-payment/<int:article_id>', views.send_request, name='request'),
#     path('verify/', views.verify, name='verify')
# ]

from django.urls import path
from . import views

urlpatterns = [
    path("request-payment/<int:article_id>/", views.send_request, name="request"),
    path("confirm/", views.confirm_payment, name="confirm_payment"),
]
