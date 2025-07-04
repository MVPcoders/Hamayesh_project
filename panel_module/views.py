from django.shortcuts import render
from account_module.models import User
from article_module.models import Article
from django.core.paginator import Paginator


def user_list(request):
    users = User.objects.all()  # تمام کاربران را استخراج کنید
    paginator = Paginator(users, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    return render(request, 'panel_module', {'users': users})


def management(request):
    users = User.objects.all()
    article_count = Article.objects.count()
    user_count = User.objects.count()
    context = {
        'users': users,
        'user_count': user_count,
        'article_count': article_count
    }
    return render(request, 'panel_module/management.html', context)
