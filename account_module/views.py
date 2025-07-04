from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, FormView, TemplateView
from account_module.forms import SignupModelForm, LoginForm
from .models import User


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


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'account_module/login_singnup.html'
    success_url = reverse_lazy('index')


    def form_valid(self, form):
        mobile = form.cleaned_data.get('mobile')
        password = form.cleaned_data.get('password')
        user = User.objects.filter(mobile__iexact=mobile).first()
        if user is not None:
            password_validation = user.check_password(password)
            if password_validation:
                login(self.request, user)
                return super().form_valid(form)
            else:
                form.add_error('password','تلفن همراه یا رمز عبور اشتباه است')
                return self.form_invalid(form)
        else:
            form.add_error('password', 'تلفن همراه یا رمز عبور اشتباه است')
            return self.form_invalid(form)



    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('index'))


class UserProfileView(TemplateView):
    template_name = 'account_module/user_profile.html'
