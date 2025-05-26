from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from account_module.forms import SignupModelForm


# Create your views here.

class SignUpView(CreateView):
    form_class = SignupModelForm
    template_name = 'account_module/login_singnup.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save(commit=False)
        user_password = form.cleaned_data.get('password')
        user_code_meli = form.cleaned_data.get('code_meli')
        user.is_active = True
        user.set_password(user_password)
        user.username = user_code_meli
        user.save()
        return super().form_valid(form)
