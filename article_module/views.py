from logging import raiseExceptions
import os
from random import random
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.detail import DetailView
from hamayesh_module.models import Hamayesh_prices
from .models import Article
import qrcode
from django.core.files.base import ContentFile
from io import BytesIO
import base64
from django.views.decorators.csrf import csrf_exempt
import json




# دکوریتور ها
def is_login(func):
    def wrapper(request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse('login'))

    return wrapper




@method_decorator(is_login, name='dispatch')
class SubmitArticle(View):
    def get(self, request, *args, **kwargs):
        return render(request, "article_moddule/article.html", context={})

    def post(self, request, *args, **kwargs):
        ar_price = int(Hamayesh_prices.objects.get(is_active=True).price)

        try:
            form = request.POST
            authors_info = {}
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

            article = Article.objects.create(
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

            # ساخت لینک مقاله
            article_url = request.build_absolute_uri(article.get_absolute_url())

            # ساخت QR Code
            qr = qrcode.make(article_url)
            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            file_name = f"article_{article.id}_qrcode.png"
            article.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=True)

            return JsonResponse({
                'status': 'success',
                'message': 'مقاله با موفقیت ثبت گردید',
                'qr_code_url': article.qr_code.url
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })


class ArticleDetailView(DetailView):
    model = Article
    template_name = "article_moddule/article_cer.html"
    context_object_name = "article"


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


@is_login
def generate_certificate(request):
    articles = Article.objects.filter(is_coached=True)
    if request.method == "POST":
        article_id = request.POST.get("article_id")
        cert_type = request.POST.get("certificate_type")
        article = get_object_or_404(Article, id=article_id, user=request.user)

    return render(request, "article_moddule/article_cer_maker.html", {"articles": articles})


@csrf_exempt
def save_certificate(request):
    if request.method == "POST":
        data = json.loads(request.body)
        article_id = data.get("article_id")
        cert_type = data.get("cert_type")
        image_data = data.get("image")

        article = Article.objects.get(id=article_id)

        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        file_data = ContentFile(base64.b64decode(imgstr), name=f"{cert_type}_{article_id}.{ext}")

        if cert_type == "cert1":
            article.certificate_file = file_data
        elif cert_type == "cert2":
            article.paziresh_file = file_data
        elif cert_type == "cert3":
            article.kargah_file = file_data

        article.save()
        return JsonResponse({"status": "success"})
