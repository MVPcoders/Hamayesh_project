from django.urls import path
from .views import multi_step_form

urlpatterns = [
    path('new-article/', multi_step_form, name='new_article'),
    # other paths...
]
