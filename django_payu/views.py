import json

from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http.response import JsonResponse

from django_payu.core import DjangoPay
from django_payu.models import PayuPayment
from django_payu.decorators import require_JSON, require_AJAX
from django_payu.helpers import ErrorMessages, NoParamException, BadParamValueException, PaymentStatus


@csrf_exempt
@require_POST
@require_JSON
def start_payment(request):
    json_str = request.body.decode('utf-8')
    data = json.loads(json_str)

    user_id = data.get("user_id")
    quantity = data.get("quantity")
    price = data.get("price")
    title = data.get("title")

    if not user_id:
        raise NoParamException(ErrorMessages.USER_ID_NOT_FOUND)
    if not quantity:
        raise NoParamException(ErrorMessages.QUANTITY_NOT_FOUND)
    if not price:
        raise NoParamException(ErrorMessages.PRICE_NOT_FOUND)
    if not title:
        raise NoParamException(ErrorMessages.TITLE_NOT_FOUND)
    try:
        User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise BadParamValueException(ErrorMessages.USER_NOT_FOUND)

    user = User.objects.get(pk=user_id)

    new_payment = DjangoPay.create_payu_payment(title, price, quantity, user, request.META["REMOTE_ADDR"])

    response = {
        "order_id": new_payment.uid,
        "payu_id": new_payment.payu_id,
        "follow": new_payment.payu_url,
    }
    return JsonResponse(response)


@csrf_exempt
@require_POST
@require_JSON
def payu_notify(request):
    body = request.body
    data = json.loads(body.decode("utf-8"))
    if "order" not in data:
        raise BadParamValueException(ErrorMessages.BAD_JSON_STRUCTURE)
    order = data["order"]

    if "orderId" not in order:
        raise BadParamValueException(ErrorMessages.ORDER_ID_NOT_FOUND)
    if "extOrderId" not in order:
        raise BadParamValueException(ErrorMessages.EXT_ORDER_ID_NOT_FOUND)
    if "status" not in order:
        raise BadParamValueException(ErrorMessages.STATUS_NOT_FOUND)

    order_id = order["orderId"]
    payment_id = order["extOrderId"]
    status = order["status"]

    try:
        payment = PayuPayment.objects.get(
            uid=payment_id,
            payu_id=order_id,
        )
    except PayuPayment.DoesNotExist:
        raise BadParamValueException(ErrorMessages.PAYMENT_NOT_FOUND)

    if status == "COMPLETED":
        payment.status = PaymentStatus.STATUS_COMPLETED
    elif status == "CANCELED":
        payment.status = PaymentStatus.STATUS_FAILED
    elif status == "PENDING":
        if payment.status not in[PaymentStatus.STATUS_COMPLETED, PaymentStatus.STATUS_FAILED]:
            payment.status = PaymentStatus.STATUS_STARTED
    payment.save()
    return JsonResponse({})


def payu_continue(request, payment_id):
    request.session["payment_id"] = payment_id
    return redirect('django_pay_complete')


@require_AJAX
def payu_status(request, payment_id):
    try:
        payment = PayuPayment.objects.get(pk=payment_id)
    except PayuPayment.DoesNotExist:
        raise BadParamValueException(ErrorMessages.PAYMENT_NOT_FOUND)

    data = {
        "status": payment.status
    }
    return JsonResponse(data)