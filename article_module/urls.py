from django.urls import path
from .views import multi_step_form

urlpatterns = [
    path('multi-step-form/', multi_step_form, name='multi_step_form'),
    # other paths...
]
