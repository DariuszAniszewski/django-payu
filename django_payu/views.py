import json

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http.response import JsonResponse

from django_payu.models import PayuPayment
from django_payu.decorators import require_JSON
from django_payu.helpers import ErrorMessages, BadParamValueException, PaymentStatus, Logger


@csrf_exempt
@require_POST
@require_JSON
def payu_notify(request):
    body = request.body
    Logger.i("PayU notification body: {}".format(body.decode("utf-8")))
    data = json.loads(body.decode("utf-8"))
    if "order" not in data:
        Logger.e("Key order not found")
        raise BadParamValueException(ErrorMessages.BAD_JSON_STRUCTURE)
    order = data["order"]

    if "orderId" not in order:
        Logger.e("Key orderId not found")
        raise BadParamValueException(ErrorMessages.ORDER_ID_NOT_FOUND)
    if "extOrderId" not in order:
        Logger.e("Key extOrderId not found")
        raise BadParamValueException(ErrorMessages.EXT_ORDER_ID_NOT_FOUND)
    if "status" not in order:
        Logger.e("Key status not found")
        raise BadParamValueException(ErrorMessages.STATUS_NOT_FOUND)

    payu_id = order["orderId"]
    payment_id = order["extOrderId"]
    payment_status = order["status"]

    try:
        payment = PayuPayment.objects.get(
            payment_id=payment_id,
            payu_id=payu_id,
        )
    except PayuPayment.DoesNotExist:
        raise BadParamValueException(ErrorMessages.PAYMENT_NOT_FOUND)

    if payment_status == "COMPLETED":
        payment.payment_status = PaymentStatus.STATUS_COMPLETED
    elif payment_status == "CANCELED":
        payment.payment_status = PaymentStatus.STATUS_FAILED
    elif payment_status == "PENDING":
        if payment.payment_status not in [PaymentStatus.STATUS_COMPLETED, PaymentStatus.STATUS_FAILED]:
            payment.payment_status = PaymentStatus.STATUS_STARTED
    payment.save()
    return JsonResponse({})
