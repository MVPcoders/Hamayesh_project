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
import logging
from django.urls import reverse
from azbankgateways import (
    bankfactories,
    models as bank_models,
    default_settings as settings,
)
from azbankgateways.exceptions import AZBankGatewaysException


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




def go_to_gateway_view(request):
    # خواندن مبلغ از هر جایی که مد نظر است
    amount = 1000000
    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    user_mobile_number = "+989112221234"  # اختیاری

    factory = bankfactories.BankFactory()
    try:
        bank = (
            factory.auto_create()
        )  # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(amount)

        # در صورت تمایل می توانید داده های دلخواه خود را به درگاه ارسال کنید
        bank.set_custom_data({"foo": "bar"})


        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        bank.set_client_callback_url(reverse("call"))
        bank.set_mobile_number(user_mobile_number)  # اختیاری

        # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
        # پرداخت برقرار کنید.
        bank_record = bank.ready()

        # هدایت کاربر به درگاه بانک
        return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        logging.critical(e)
        # TODO: redirect to failed page.
        raise e


def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
        # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.
        return HttpResponse("پرداخت با موفقیت انجام شد.")

    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    return HttpResponse(
        "پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت."
    )





