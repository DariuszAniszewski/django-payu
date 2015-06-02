import json

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email, validate_ipv4_address

from django_payu.helpers import DjangoPayException, ErrorMessages

from django_payu.api import PayUApi
from django_payu.models import PayuPayment


class DjangoPayU:
    @classmethod
    def create_payu_payment(cls, buyer, product, description, continue_url):

        payment = PayuPayment()

        payment.buyer_first_name = buyer.first_name
        payment.buyer_last_name = buyer.last_name
        payment.buyer_email = buyer.email
        payment.buyer_ip_address = buyer.ip_address
        payment.payment_description = description

        payment.product_name = product.name
        payment.product_unit_price = product.unit_price
        payment.product_quantity = product.quantity

        payment.continue_url = continue_url

        payment.save()

        api = PayUApi(settings.DJANGO_PAYU_POS_ID, settings.DJANGO_PAYU_POS_AUTHORIZATION_KEY)
        response_code, response_data = api.make_order(payment)
        response_dict = json.loads(response_data.decode('utf-8'))
        payment.payu_id = response_dict["orderId"]
        payment.payment_status = "started"
        payment.save()

        follow = response_dict["redirectUri"]

        return payment.payment_id, follow

    @classmethod
    def get_payment_status(cls, payment_id):
        try:
            return PayuPayment.objects.get(pk=payment_id).payment_status
        except PayuPayment.DoesNotExist:
            raise DjangoPayException(ErrorMessages.PAYMENT_NOT_FOUND)


class Buyer:
    first_name = None
    last_name = None
    email = None
    ip_address = None

    def __init__(self, first_name, last_name, email, ip_address):
        self.first_name = first_name
        self.last_name = last_name
        self.email = self.__ensure_is_email_address(email)
        self.ip_address = self.__ensure_is_ip_address(ip_address)

    @staticmethod
    def __ensure_is_email_address(email):
        try:
            validate_email(email)
        except ValidationError:
            raise DjangoPayException(ErrorMessages.NOT_VALID_EMAIL_ADDRESS)
        return email

    @staticmethod
    def __ensure_is_ip_address(ip_address):
        try:
            validate_ipv4_address(ip_address)
        except ValidationError:
            raise DjangoPayException(ErrorMessages.NOT_VALID_IP_ADDRESS)
        return ip_address


class Product:
    name = None
    unit_price = None
    quantity = None

    def __init__(self, name, unit_price, quantity):
        self.name = name
        self.unit_price = self.__ensure_is_int(unit_price, ErrorMessages.NOT_VALID_UNIT_PRICE)
        self.quantity = self.__ensure_is_int(quantity, ErrorMessages.NOT_VALID_QUANTITY)

    @staticmethod
    def __ensure_is_int(value, error_message):
        if isinstance(value, int):
            return value
        elif isinstance(value, str) or isinstance(value, bytes):
            try:
                return int(value)
            except ValueError:
                raise DjangoPayException(error_message)
        else:
            raise DjangoPayException(error_message)