from django.urls import path
from . import views

urlpatterns=[
    path('signup', views.SignUpView.as_view(), name='signup'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('profile', views.UserProfileView, name='profile'),
    # path('new-ticket/', views.new_ticket, name='new-ticket'),
    # path('tickets/', views.tickets_list, name='tickets'),
    # path('tickets/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
]