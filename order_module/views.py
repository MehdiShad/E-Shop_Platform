import json
import time
from pprint import pprint
import requests
from django.urls import reverse
from django.conf import settings
from product_module.models import Product
from django.shortcuts import render, redirect
from order_module.models import Order, OrderDetail
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse

# Create your views here.

#? sandbox merchant
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'


ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

amount = 1000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
phone = 'YOUR_PHONE_NUMBER'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/order/verify-payment/'


def add_product_to_order(request: HttpRequest):
    product_id = int(request.GET.get('product_id'))
    count = int(request.GET.get('count'))
    if count < 1:
        return JsonResponse({
            'status': 'invalid count',
            'text': 'مقدار وارد شده معتبر نمیباشد.',
            'confirm_button_text': 'مرسی از شما',
            'icon': 'warning',
        })

    if request.user.is_authenticated:
        product = Product.objects.filter(id=product_id, is_delete=False, is_active=True).first()
        if product is not None:
            current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
            current_order_detail = current_order.orderdetail_set.filter(product_id=product_id).first()
            if current_order_detail is not None:
                current_order_detail.count += count
                current_order_detail.save()
            else:
                new_detail = OrderDetail(order_id=current_order.id, product_id=product_id, count=count)
                new_detail.save()
            return JsonResponse({
                'status': 'success',
                'text': 'محصول مورد نظر با موفقیت به سبد خرید شما اضافه شد.',
                'confirm_button_text': 'باشه ممنون',
                'icon': 'success',
            })

        else:
            return JsonResponse({
                'status': 'not_found',
                'text': 'محصول مورد نظر یافت نشد',
                'confirm_button_text': 'باشه',
                'icon': 'error',
            })
    else:
        return JsonResponse({
            'status': 'not_auth',
            'text': 'برای افزودن محصول به سبد خرید، باید وارد سایت شوید.',
            'confirm_button_text': 'ورود به سایت',
            'icon': 'error',
        })


@login_required
def request_payment(request: HttpRequest):
    #todo: add request logger for payments
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_order_price = current_order.calculate_total_price()
    if total_order_price == 0:
        return redirect(reverse('user_basket_page'))

    data = {
        "MerchantID": settings.MERCHANT,
        # "Amount": total_order_price,
        "Amount": 2000,
        "Description": description,
        # "Phone": phone,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    print('data', data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
        print("response")
        pprint(response)
        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                # return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),'authority': response['Authority']}
                url = ZP_API_STARTPAY + str(response['Authority'])
                return redirect(f"{url}")
            else:
                return {'status': False, 'code': str(response['Status'])}
        return response

    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}
    except Exception as ex:
        return {'status': False, 'code': str(ex)}


@login_required
def verify_payment(request: HttpRequest):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_order_price = current_order.calculate_total_price()
    t_authority = request.GET['Authority']
    data = {
        "MerchantID": settings.MERCHANT,
        # "Amount": total_order_price * 10,
        "Amount": 2000,
        "Authority": t_authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
    #todo : complete verify
    if response.status_code == 200:
        t_status = response.json()
        if t_status['Status'] == 100:
            current_order.is_paid = True
            current_order.payment_date = time.time()
            current_order.save()
            context = {
                'success': True,
                'message': f"تراکنش شما با کد پیگیری {response.json()['data']['code']} با موفقیت انجام شد."
            }
            return render(request, 'order_module/payment_result.html', context=context)
            # return {'status': True, 'RefID': response['RefID']}
        else:
            # return {'status': False, 'code': str(response['Status'])}
            context = {
                'success': False,
                'message': f"خطا {response.json()}"
            }
            return render(request, 'order_module/payment_result.html', context=context)
    return response

