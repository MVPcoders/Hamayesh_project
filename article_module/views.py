from logging import raiseExceptions
import os

from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from hamayesh_module.models import Hamayesh_prices
from .models import Article


# دکوریتور ها
def is_login(func):
    def wrapper(request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse('login'))

    return wrapper


# def user_authenticator(func):
#     def wrapper(request: HttpRequest, *args, **kwargs):
#         try:
#             Article.objects.get(user = request.user.id , id = request.GET.get('article_id'))
#             return func(request, *args, **kwargs)
#         except:
#             return redirect(reverse('index'))
#
#     return wrapper


@method_decorator(is_login, name='dispatch')
class SubmitArticle(View):

    def get(self, request, *args, **kwargs):
        return render(request, "article_moddule/article.html", context={})

    def post(self, request, *args, **kwargs):
        ar_price = int(Hamayesh_prices.objects.get(is_active=True).price)
        try:
            form = request.POST
            authors_info = {}
            # برای تشخیص نویسنده مسئول
            corresponding_author_index = int(form.get('correspondingAuthor', 0))
            author_count = int(form['authorCount'])
            for i in range(author_count):
                authour = {
                    "first_name": form.get(f'authorFirstName{i}'),
                    "last_name": form.get(f'authorLastName{i}'),
                    "email": form.get(f'authorEmail{i}'),
                    "codemeli": form.get(f'authorCodemeli{i}'),
                    "main_author": (i == corresponding_author_index),
                }
                authors_info[i] = authour

            Article.objects.create(
                user=request.user,
                authors_numbers=form['authorCount'],
                main_goal=form['articleMainGoal'],
                language=form['articleLang'],
                persian_subject=form['articlePersianTitle'],
                english_subject=form['articleEnglishTitle'],
                article_abstract=form['articleAbstract'],
                file=request.FILES.get('articleFile'),
                authors_info=authors_info,
                price=ar_price
            )
            return JsonResponse({
                'status': 'success',
                'message': 'مقاله با موفقیت ثبت گردید'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'success',
                'message': str(e)
            })


@method_decorator(is_login, name='dispatch')
class UserArticleEdit(View):
    def get(self, request):
        context = {}
        return render(request, 'account_module/user_profile.html', context)

    def post(self, request):
        try:
            form = request.POST
            article: Article = Article.objects.filter(user_id=request.user.id, id=form.get('articleId')).first()
            if request.FILES.get('newFile'):
                if article.file:
                    if os.path.isfile(article.file.path):
                        os.remove(article.file.path)
                article.file = request.FILES.get('newFile')

            article.persian_subject = form.get('editPersianTitle')
            article.english_subject = form.get('editEnglishTitle')
            article.main_goal = form.get('editMainGoal')
            article.language = form.get('editLanguage')
            article.article_abstract = form.get('editAbstract')

            article.save()
            return JsonResponse({
                'status': 'success',
                'message': 'مقاله شما با موفقیت ویرایش شد'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'fail',
                'message': str(e)
            })


@is_login
def user_delete_article(request):
    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        raise Http404()
    try:
        article_id = request.GET.get('article_id')
        article = Article.objects.get(id=article_id, user=request.user)
        if article.file:
            if os.path.isfile(article.file.path):
                os.remove(article.file.path)
        article.delete()
        return JsonResponse({
            'status': 'success',
            'message': 'مقاله با موفقیت حذف شد.'
        })
    except:
        return JsonResponse({
            'status': "error",
            'message': "خطایی رخ داده"
        })


@is_login
def send_correction_request(request):
    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        raise Http404()
    try:
        article = Article.objects.get(id=request.GET.get('article_id'), user=request.user)
        if article.need_correction:
            article.need_correction = False
            article.is_corrected = True
            article.save()
            return JsonResponse({
                'status': 'success',
                'text': 'درخواست با موفقیت ارسال شد',
                'icon': 'success'
            })
        return JsonResponse({
            'status': 'error',
            'text': 'درخواست شما معتبر نیست. کد:500',
            'icon': 'error'
        })
    except:
        return JsonResponse({
            'status': 'error',
            'text': 'درخواست شما معتبر نیست. کد: 501',
            'icon': 'error'
        })
