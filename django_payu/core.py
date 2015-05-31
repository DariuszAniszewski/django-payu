import json

from django.conf import settings

from django_payu.helpers import DjangoPayException, ErrorMessages

from django_payu.payu import PayUApi
from django_payu.models import PayuPayment


class NewPayUPurchase:
    uid = None
    payu_id = None
    payu_url = None

    def __init__(self, uid, payu_id, payu_url):
        self.uid = uid
        self.payu_id = payu_id
        self.payu_url = payu_url


class DjangoPay:
    @classmethod
    def create_payu_payment(cls, title, total_unit_price, quantity, user, ip_address):
        total_unit_price = DjangoPay.__ensure_is_int(total_unit_price, ErrorMessages.PRICE_MALFORMED)
        quantity = DjangoPay.__ensure_is_int(quantity, ErrorMessages.QUANTITY_MALFORMED)

        payment = PayuPayment()
        payment.name = title
        payment.price = total_unit_price
        payment.quantity = quantity
        payment.user = user
        payment.ip_address = ip_address
        payment.save()

        api = PayUApi(settings.DJANGO_PAYU_POS_ID, settings.DJANGO_PAYU_POS_AUTHORIZATION_KEY)
        response_code, response_data = api.make_order(payment)
        response_dict = json.loads(response_data.decode('utf-8'))
        payment.payu_id = response_dict["orderId"]
        payment.status = "started"
        payment.save()

        follow = response_dict["redirectUri"]

        return NewPayUPurchase(payment.uid, payment.payu_id, follow)

    @classmethod
    def __ensure_is_int(cls, value, error_message):
        try:
            return int(value)
        except ValueError:
            raise DjangoPayException(error_message)