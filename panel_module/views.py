from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render
from account_module.models import User  # اطمینان حاصل کنید که مدل User را به درستی وارد کرده‌اید




def user_list(request):
    users = User.objects.all()  # تمام کاربران را استخراج کنید
    return render(request, 'panel_module', {'users': users})


def management(request):
    users = User.objects.all()
    context = {
        'users': users,

    }
    return render(request, 'panel_module/management.html', context)

