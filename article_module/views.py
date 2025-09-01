import string
from logging import raiseExceptions
import os
import random
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from hamayesh_module.models import Hamayesh_prices
from .models import Article
import qrcode
from django.core.files.base import ContentFile
from io import BytesIO
import base64
from django.views.decorators.csrf import csrf_exempt
import json
import io
import json
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image


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

            def generate_unique_code():
                return ''.join(random.choices(string.digits, k=10))

            unique_code = generate_unique_code()

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
                price=ar_price,
                unique_code=unique_code
            )

            article_url = request.build_absolute_uri(article.get_absolute_url())

            # ساخت QR Code
            qr = qrcode.make(article_url)
            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            file_name = f"article_{article.unique_code}_qrcode.png"
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





class VerifyArticle(View):
    def get(self, request, code):
        article = get_object_or_404(Article, unique_code=code)
        return render(request, "article_moddule/article_cer.html", {"article": article})


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


@method_decorator(is_login, name='dispatch')
class GenerateCertificate(View):
    def get(self, request):
        articles = Article.objects.filter(is_paid=True)

        # خروجی نهایی برای فرانت
        article_list = []
        for article in articles:
            if article.qr_code and not article.kargah_file:
                article_list.append({
                    "id": article.id,
                    "title": article.persian_subject,
                    'qr_code': article.qr_code.url,
                    'unique_code': article.unique_code,
                    'submit_date': article.submit_date,
                    # authors_info رو به JSON واقعی تبدیل می‌کنیم
                    "authors_info": json.dumps(article.authors_info, ensure_ascii=False),
                })

        return render(request, "article_moddule/article_cer_maker.html", {"articles": article_list})





@csrf_exempt
def save_certificate(request):
    if request.method == "POST":
        article_id = request.POST.get("article_id")
        cert_type = request.POST.get("cert_type")
        files = request.FILES.getlist("images")

        article = Article.objects.get(id=article_id)

        PAGE_WIDTH, PAGE_HEIGHT = 1368, 1000
        pdf_buffer = io.BytesIO()
        pdf = canvas.Canvas(pdf_buffer, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

        for f in files:
            # تصویر رو با Pillow باز می‌کنیم
            img = Image.open(f)

            # کاهش کیفیت و اندازه
            img = img.convert("RGB")  # اطمینان از RGB بودن
            img.thumbnail((PAGE_WIDTH, PAGE_HEIGHT), Image.LANCZOS)

            # ذخیره در حافظه با کیفیت پایین‌تر
            img_io = io.BytesIO()
            img.save(img_io, format="JPEG", quality=60, optimize=True)  # کیفیت بین 40 تا 70 تست کن
            img_io.seek(0)

            # تبدیل دوباره به ImageReader برای ReportLab
            image = ImageReader(img_io)
            pdf.drawImage(image, 0, 0, width=PAGE_WIDTH, height=PAGE_HEIGHT)
            pdf.showPage()

        pdf.save()
        pdf_buffer.seek(0)

        file_data = ContentFile(pdf_buffer.read(), name=f"{cert_type}_{article_id}.pdf")

        if cert_type == "cert1":
            article.certificate_file = file_data
        elif cert_type == "cert2":
            article.paziresh_file = file_data
        elif cert_type == "cert3":
            article.kargah_file = file_data

        article.save()
        return JsonResponse({"status": "success"})
