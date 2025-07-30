from django.urls import path
from panel_module import views


urlpatterns = [
    path('', views.ManagementView.as_view(), name='management'),
    path('change-pass', views.ChangePasswordView.as_view(), name='change_password'),

]
