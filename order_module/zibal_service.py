import requests
import json

ZIBAL_REQUEST_URL = "https://gateway.zibal.ir/v1/request"
ZIBAL_VERIFY_URL = "https://gateway.zibal.ir/v1/verify"
ZIBAL_STARTPAY = "https://gateway.zibal.ir/start/{trackId}"

MERCHANT = "6878e814a45c72001aa408b7"  # تستی، بعداً مرچنت اصلیت رو بذار
# MERCHANT = "zibal"  # تستی، بعداً مرچنت اصلیت رو بذار


def zibal_send_request(amount, callback_url, description="پرداخت هزینه", order_id=None, mobile=None):
    data = {
        "merchant": MERCHANT,
        "amount": amount,
        "callbackUrl": callback_url,
        "description": description,
    }
    if order_id:
        data["orderId"] = str(order_id)
    if mobile:
        data["mobile"] = str(mobile)

    headers = {"content-type": "application/json"}
    response = requests.post(ZIBAL_REQUEST_URL, data=json.dumps(data), headers=headers)
    res_json = response.json()

    if res_json.get("result") == 100:
        # موفق -> باید کاربر رو به این لینک بفرستیم
        return True, res_json["trackId"]
    else:
        return False, res_json.get("message", "خطا در ارتباط با درگاه")


def verify_payment(track_id, amount):
    data = {
        "merchant": MERCHANT,
        "trackId": track_id,
    }
    headers = {"content-type": "application/json"}
    response = requests.post(ZIBAL_VERIFY_URL, data=json.dumps(data), headers=headers)
    res_json = response.json()

    if res_json.get("result") == 100 and res_json.get("amount") == amount:
        # پرداخت موفق
        return True, res_json.get("refNumber")
    elif res_json.get("result") == 201:
        # تراکنش قبلاً پرداخت شده
        return "duplicate", res_json.get("refNumber")
    else:
        return False, res_json.get("message", "پرداخت ناموفق")
