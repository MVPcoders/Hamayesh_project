from django.contrib.auth import login, logout
from django.http import HttpRequest
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, FormView
from account_module.forms import SignupModelForm, LoginForm
from .models import User
from article_module.models import Article
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TicketForm
from .models import Ticket


def login_for_ticket(func):
    def wrapper(request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse('login'))

    return wrapper


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
                form.add_error('password', 'تلفن همراه یا رمز عبور اشتباه است')
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

@login_required(login_url='login')
def UserProfileView(request):
    articles = Article.objects.filter(user=request.user).all()
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, 'تیکت شما با موفقیت ثبت شد.')
            return redirect('profile')
    else:
        form = TicketForm()
    tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'articles': articles,
        'form': form,
        'tickets': tickets
    }
    return render(request, 'account_module/user_profile.html', context)

