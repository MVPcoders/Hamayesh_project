import json
import time
from importlib.metadata import metadata
from os import times
from datetime import datetime
from django.contrib.auth.decorators import login_required
import requests
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.db import models
from article_module.models import Article
from hamayesh_module.models import Hamayesh_prices
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Payment, DiscountCode
from account_module.forms import DiscountCodeForm
from order_module.utils import apply_discount
from django.contrib import messages

def pay(request):
    return render(request, "order_module/pay.html", context={})





merchant_id = "3a681e90-59c0-4511-8101-655b26314ae5"
ZP_API_REQUEST = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://sandbox.zarinpal.com/pg/StartPay/{authority}"
callback_url = "self.callbackURL"
description = "نهایی کردن خرید شما از سایت ما"
mobile = "mobile"  # اختیاری
email = "email"  # اختیاری
CallbackURL = 'http://localhost:8000/pay/verify/'

def apply_discount_view(request,article_id):
    if request.method == "POST":
        article, created = Article.objects.get_or_create(is_paid=False, user=request.user.id, id=article_id)
        form = DiscountCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                discount_code = DiscountCode.objects.get(code=code)
                if discount_code.is_valid(request.user):
                    price = article.price
                    new_total = apply_discount(price, discount_code)
                    article.price = new_total
                    article.save()
                    messages.success(request,f'کد تخفیف {discount_code.discount_percent} درصدی با موفقیت اعمال شد !')
                    return redirect('profile')
            except DiscountCode.DoesNotExist:
                messages.error(request, "کد تخفیف نامعتبر است!")
                return redirect('profile')
    messages.error(request, "خطایی رخ داده است!")
    return redirect('profile')

@login_required
def send_request(request: HttpRequest, article_id):
    article_payment, created = Article.objects.get_or_create(is_paid=False, user=request.user.id, id=article_id)
    price = int(article_payment.price)
    req_data = {
        "merchant_id": merchant_id,
        "amount": price,
        "callback_url": CallbackURL,
        "description": description,
        # metadata: {"mobile": request.user.mobile,"email":request.user.email},
    }
    req_headers = {"accept": "application/json", "content-type": "application/json"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_headers)
    authority = req.json()['data']['authority']
    article_payment.send_to_pay = authority
    article_payment.save()
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        errors = req.json()['errors']['errors']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"error code : {errors}, error message: {e_message}")


@login_required
def verify(request: HttpRequest):
    t_authority = request.GET['Authority']
    article_payment = Article.objects.get(send_to_pay=t_authority, user=request.user.id)
    price = int(article_payment.price)
    if request.GET.get('Status') == 'OK':
        req_headers = {"accept": "application/json", "content-type": "application/json"}
        req_data = {"merchant_id": merchant_id,
                    "amount": price,
                    "authority": t_authority, }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_headers)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            req_id = req.json()["data"]["ref_id"]
            if t_status == 100:

                article_payment.is_paid = True
                article_payment.save()
                amount = price
                user = request.user if request.user.is_authenticated else None
                payment = Payment.objects.create(
                    user=user,
                    amount=amount,
                    is_successful=True,
                    transaction_id=req_id
                )
                return render(request, 'order_module/pay.html', {
                    'success': f"{req_id}",
                    'amount': price,
                    'date': datetime.now(),
                })
            elif t_status == 101:
                return render(request, 'order_module/pay.html', {
                    'info': f"این تراکنش قبلا انجام شده ",
                })
            else:
                return redirect('index')
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return render(request, 'order_module/pay.html', {
                'info': f"{e_message}",
            })
    else:
        return render(request, 'order_module/pay.html', )










