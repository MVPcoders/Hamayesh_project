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


merchant_id = "7fed38ae-39b5-49f5-8019-d5912ffea009"
ZP_API_REQUEST = "https://payment.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://payment.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://payment.zarinpal.com/pg/StartPay/{authority}"
callback_url = "self.callbackURL"
description = "نهایی کردن خرید شما از سایت ما"
mobile = "mobile"  # اختیاری
email = "email"  # اختیاری
CallbackURL = 'http://127.0.0.1:8000/order/verify/'


@login_required
def send_request(request: HttpRequest):
    # current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    # total_price, total_discount = current_order.calculate_total_price()
    # if total_price == 0:
    #     return redirect(reverse("basket"))
    price = 5_000_000
    req_data = {
        "merchant_id": merchant_id,
        "amount": price,
        "callback_url": CallbackURL,
        "description": description,
        # metadata: {"mobile": mobile,"email":email},
    }
    req_headers = {"accept": "application/json", "content-type": "application/json"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_headers)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        errors = req.json()['errors']['errors']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"error code : {errors}, error message: {e_message}")


@login_required
def verify(request: HttpRequest):
    price = 5_000_000
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_headers = {"accept": "application/json", "content-type": "application/json"}
        req_data = {"merchant_id": merchant_id,
                    "amount": price,
                    "authority": t_authority, }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_headers)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            req_id = req.json()["data"]["ref_id"]
            if t_status == '100':

                return render(request, 'order_module/payment_result.html', {
                    'success': f"تراکنش با کد پیگیری {req_id} با موفقیت انجام شد ",
                })
            elif t_status == '101':
                return render(request, 'order_module/payment_result.html', {
                    'info': f"این تراکنش قبلا انجام شده ",
                })
            else:
                return redirect('user_profile')
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return render(request, 'order_module/payment_result.html', {
                'info': f"{e_message}",
            })
    else:
        return redirect('home_page')

# Create your views here.





