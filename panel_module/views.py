from audioop import reverse

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View

from account_module.models import User
from article_module.models import Article
from django.core.paginator import Paginator
from django.db.models import Sum
from datetime import datetime, timedelta
from order_module.models import Payment


def user_list(request):
    users = User.objects.all()  # تمام کاربران را استخراج کنید
    paginator = Paginator(users, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    return render(request, 'panel_module', {'users': users})

class ManagementView(TemplateView):
    template_name = 'panel_module/management.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.now()
        first_day = today.replace(day=1)
        last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        # Calculate current month sales
        current_month_sales = Payment.objects.filter(
            payment_date__range=[first_day, last_day],
            is_successful=True
        ).aggregate(total_sales=Sum('amount'))['total_sales'] or 0

        # Monthly summary
        monthly_data = []
        for i in range(12):  # Last 12 months
            month = today.month - i
            year = today.year
            if month < 1:
                month += 12
                year -= 1

            first_day_month = datetime(year, month, 1)
            last_day_month = (first_day_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

            monthly_sum = Payment.objects.filter(
                payment_date__range=[first_day_month, last_day_month],
                is_successful=True
            ).aggregate(total=Sum('amount'))['total'] or 0

            monthly_data.append({
                'year': year,
                'month': month,
                'total_sales': monthly_sum
            })

        context.update({
            'users': User.objects.all(),
            'user_count': User.objects.count(),
            'article_count': Article.objects.count(),
            'articles': Article.objects.all(),
            'current_month_sales': current_month_sales,
            'monthly_data': monthly_data,
        })
        return context


class ChangePasswordView(View):
    def get (self, request):
        users = User.objects.all()
        context = {'users': users}
        return render(request, 'panel_module/change_password.html', context)

    def post(self, request):
        try:
            user = User.objects.get(id = request.POST['user_id'])
            user.set_password(request.POST['new_password'])
            user.save()
            return redirect('/management/?success=1')
        except Exception as e:
            return JsonResponse({'error': str(e)})



